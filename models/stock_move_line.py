# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _action_done(self):
        res = super(StockMoveLine, self)._action_done()
        for i in self:
            if i.move_id.production_id.flyt_mo_order_type == 'remanufacturing':
                i.move_id.production_id.finished_move_line_ids.unlink()
            self = self.filtered(lambda l: l.exists())
        for line in self:
            if line.move_id:
                move = line.move_id
                if move.flyt_operation == 'remove':
                    line.location_dest_id = line.location_id
                elif move.flyt_operation == 'recycle':
                    line.location_id, line.location_dest_id = line.location_dest_id, line.location_id
        return res
