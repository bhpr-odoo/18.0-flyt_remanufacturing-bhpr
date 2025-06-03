# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class MrpStockReport(models.TransientModel):
    _inherit = 'stock.traceability.report'

    @api.model
    def get_lines(self, line_id=False, **kw):
        context = dict(self.env.context)
        model = kw and kw['model_name'] or context.get('model')
        rec_id = kw and kw['model_id'] or context.get('active_id')
        level = kw and kw['level'] or 1
        lines = self.env['stock.move.line']

        record = self.env[model].browse(rec_id)
        if model == 'mrp.production' and record.flyt_mo_order_type == 'remanufacturing':
            lines = record.move_raw_ids.mapped('move_line_ids').filtered(lambda m: m.state == 'done')
            move_line_vals = self._lines(line_id, model_id=rec_id, model=model, level=level, move_lines=lines)
            final_vals = sorted(move_line_vals, key=lambda v: v['date'], reverse=True)
            lines = self._final_vals_to_lines(final_vals, level)
            return lines
        else:
            return super().get_lines(line_id=line_id, **kw)
