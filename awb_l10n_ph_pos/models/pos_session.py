from odoo import api, fields, models


class PosSession(models.Model):
    _inherit = "pos.session"

    awb_cash_difference = fields.Monetary(
        string="Cash Difference", store=False, compute="_compute_awb_cash_difference"
    )

    @api.depends("cash_register_id")
    def _compute_awb_cash_difference(self):
        for record in self:
            record.awb_cash_difference = 0
            if record.cash_register_id:
                account_bank_statement_line = record.cash_register_id.line_ids.filtered(
                    lambda r: "Cash difference observed during the counting"
                    in r.payment_ref
                )
                record.awb_cash_difference = sum(
                    account_bank_statement_line.mapped("amount")
                )
