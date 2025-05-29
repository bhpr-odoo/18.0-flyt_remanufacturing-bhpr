# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, _


class StockLot(models.Model):
    _inherit = 'stock.lot'

    flyt_stock_move_ids = fields.One2many('flyt.stock.lot.link', 'parent_lot_id', store=True)
