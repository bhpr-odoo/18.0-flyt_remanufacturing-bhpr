# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    flyt_mo_order_type = fields.Selection(
        [('manufacturing', 'Manufacturing'), ('remanufacturing', 'Remanufacturing')],
        string='Order Type',
        default='manufacturing',
        store=True
    )

    @api.onchange('flyt_mo_order_type')
    def _onchange_order_type_set_bom(self):
        if self.flyt_mo_order_type == 'remanufacturing' and self.product_id:
            self.bom_id = False
            reman_bom = self.env['mrp.bom'].search([
                ('type', '=', 'remanufacture'),
                ('product_tmpl_id', '=', self.product_tmpl_id.id)
            ], limit=1)
            if reman_bom:
                self.bom_id = reman_bom.id
        else:
            self.bom_id = False

    def _get_move_raw_values(self, product, product_qty, product_uom, operation_id=False, bom_line=False):
        vals = super()._get_move_raw_values(product, product_qty, product_uom, operation_id, bom_line)
        if bom_line:
            vals['flyt_operation'] = bom_line.flyt_operation
        return vals

    def _check_sn_uniqueness(self):
        if self.flyt_mo_order_type == 'remanufacturing':
            return True
        return super()._check_sn_uniqueness()

    def button_mark_done(self):
        res = super().button_mark_done()
        component_moves = self.move_raw_ids.filtered(lambda m: m.state == 'done')
        if self.lot_producing_id:
            parent_lot = self.lot_producing_id
            if self.flyt_mo_order_type == 'manufacturing':
                    for component_move in component_moves:
                        if component_move.lot_ids:
                            for lot in component_move.lot_ids:
                                self.env['flyt.stock.lot.link'].create({
                                    'parent_lot_id': self.lot_producing_id.id,
                                    'parent_lot_name': self.lot_producing_id.name,
                                    'child_lot_id':  lot.id,
                                    'child_lot_name': lot.name,
                                    'child_product_id': lot.product_id.id,
                                    'install_date': datetime.now(),
                                    'install_reference': component_move.id,
                                    'install_state': True,
                                })
                                parent_lot.message_post(body=_(
                                    "Product %s with serial number %s added", lot.product_id.name, lot.name
                                ), message_type='comment', subtype_id=False)
            elif self.flyt_mo_order_type == 'remanufacturing':
                for component_move in component_moves:
                    if component_move.lot_ids and component_move.flyt_operation == 'add':
                        for lot in component_move.lot_ids:
                            self.env['flyt.stock.lot.link'].create({
                                'parent_lot_id': self.lot_producing_id.id,
                                'parent_lot_name': self.lot_producing_id.name,
                                'child_lot_id':  lot.id,
                                'child_lot_name': lot.name,
                                'child_product_id': lot.product_id.id,
                                'install_date': datetime.now(),
                                'install_reference': component_move.id,
                                'install_state': True,
                            })
                            parent_lot.message_post(body=_(
                                    "Product %s with serial number %s added", lot.product_id.name, lot.name
                                ), message_type='comment', subtype_id=False)
                    elif component_move.lot_ids and component_move.flyt_operation in ['remove', 'recycle']:
                        for lot in component_move.lot_ids:
                            existing_link = self.env['flyt.stock.lot.link'].search([
                                    ('parent_lot_id', '=', self.lot_producing_id.id),
                                    ('child_lot_id', '=', lot.id),
                                    ('install_state', '=', True)
                                ], limit=1)
                            if existing_link:
                                existing_link.write({
                                    'remove_date': fields.Datetime.now(),
                                    'remove_reference': component_move.id,
                                    'install_state': False,
                                })
                                if component_move.flyt_operation == 'remove':
                                    parent_lot.message_post(body=_(
                                    "Product %s with serial number %s removed", lot.product_id.name, lot.name
                                ), message_type='comment', subtype_id=False)
                                elif component_move.flyt_operation == 'recycle':
                                    parent_lot.message_post(body=_(
                                    "Product %s with serial number %s recycled", lot.product_id.name, lot.name
                                ), message_type='comment', subtype_id=False)
        return res
