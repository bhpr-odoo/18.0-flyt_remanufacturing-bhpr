# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class FlytStockLotLink(models.Model):
    _name = 'flyt.stock.lot.link'
    _description = 'Serial Number Relationship'
    _inherit = ['mail.thread']

    parent_lot_id = fields.Many2one('stock.lot', string='Parent Serial', required=True, index=True)
    parent_lot_name = fields.Char(related='parent_lot_id.name', string='Parent Serial Name', store=True)
    child_lot_id = fields.Many2one('stock.lot', string='Lot/Serial Number', required=True, index=True)
    child_lot_name = fields.Char(related='child_lot_id.name', string='Child Serial Name', store=True)
    install_date = fields.Datetime(string='Created On')
    install_reference = fields.Many2one('stock.move', string='Install Reference')
    remove_date = fields.Datetime(string='Remove Date')
    remove_reference = fields.Many2one('stock.move', string='Remove Reference')
    install_state = fields.Boolean(string='Currently Installed', default=True, tracking=True)
    flyt_mo_order_line = fields.Many2one('mrp.production', ondelete='cascade')
    child_product_id = fields.Many2one('product.product', related='child_lot_id.product_id',
        string='Product', store=True)
