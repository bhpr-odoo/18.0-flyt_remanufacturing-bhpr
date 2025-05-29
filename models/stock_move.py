# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    flyt_operation = fields.Selection([
        ('add', 'Add'),
        ('remove', 'Remove'),
        ('recycle', 'Recycle')
    ], string='Operation', default='add')

    def _check_quantity(self):
        if self.raw_material_production_id and self.raw_material_production_id.flyt_mo_order_type == 'remanufacturing':
            return True
        return super()._check_quantity()
