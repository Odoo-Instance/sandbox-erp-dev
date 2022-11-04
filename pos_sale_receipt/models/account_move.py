from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one('sale.order', string='Sales Order', ondelete='cascade', copy=False)
