# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    type = fields.Selection(
        selection_add=[('remanufacture', 'Remanufacture')],
        ondelete={'remanufacture': 'set default'}
    )

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    flyt_operation = fields.Selection([
        ('add', 'Add'),
        ('remove', 'Remove'),
        ('recycle', 'Recycle')
    ], string='Operation', default='add')
