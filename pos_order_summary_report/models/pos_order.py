# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    void_reason_ids = fields.Many2many(
        string="Reason", comodel_name='void.order.reason')
    voided_order = fields.Boolean(string="Is Order voided?")
    number_of_item_sold = fields.Float(
        string="Total number of items", compute="_compute_total_number_of_item")
    vatable_tax = fields.Float(
        string="VATABLE TAX", compute="_compute_total_number_of_item", store=True)
    vat_exempt = fields.Float(
        string="VATABLE EXEMPT", compute="_compute_total_number_of_item", store=True)
    zero_rated = fields.Float(
        string="ZERO RATED", compute="_compute_total_number_of_item", store=True)
    discount = fields.Float(
        string="Discount", compute="_compute_total_number_of_item", store=True)
    payment_methods = fields.Char(
        'Payment Methods', compute="_compute_total_number_of_item", store=True)
    state = fields.Selection(selection_add=[('voided', 'Voided')])


    def _compute_total_number_of_item(self):
        for order in self:
            order.number_of_item_sold = sum(order.lines.mapped('qty'))
            if order.payment_ids:
                order.payment_methods = ",".join(
                    order.payment_ids.payment_method_id.mapped('name'))
            if order.partner_id.check_sc_pwd and order.partner_id.sh_customer_discount:
                order.discount = sum(order.lines.mapped('discount'))
            order_lines = self.env['pos.order.line'].search(
                [('order_id', '=', order.id)])
            vatable_tax_sum = 0
            vat_exempt_sum = 0
            zero_rated_sum = 0
            for line in order_lines:
                if line.tax_ids_after_fiscal_position:
                    if line.tax_ids_after_fiscal_position[0].tax_type == 'vatable':
                        order.vatable_tax = vatable_tax_sum + \
                            (line.price_unit * line.qty)
                        vatable_tax_sum = order.vatable_tax
                    if line.tax_ids_after_fiscal_position[0].tax_type == 'vat_exempt':
                        order.vat_exempt = vat_exempt_sum + \
                            (line.price_unit * line.qty)
                        vat_exempt_sum = order.vat_exempt
                    if line.tax_ids_after_fiscal_position[0].tax_type == 'zero_rated':
                        order.zero_rated = zero_rated_sum + \
                            (line.price_unit * line.qty)
                        zero_rated_sum = order.zero_rated

    def void_order(self, reasons=None):
        for order in self:
            related_invoice_id = self.env['account.move'].search(
                [('pos_order_id', '=', self.id), ('move_type', '=', 'out_invoice')], limit=1)
            ref = '%'+ related_invoice_id.name
            related_journal_record = self.env['account.move'].search(
            [('move_type', '=', 'entry'), ('ref', 'like', ref)], limit=1)

            if reasons:
                order.write({'state': 'voided', 'voided_order': True, 'void_reason_ids': reasons})
            else:
                order.write({'state': 'voided', 'voided_order': True})

            return order.env['account.move.reversal']\
                .with_context(active_model="account.move", active_ids=related_journal_record.id)\
                .create({
                    'reason': "",
                    'refund_method': 'cancel',
                    'journal_id': related_journal_record.journal_id.id,
                    'move_ids': [(4, related_journal_record.id, 0)]
                })\
                .reverse_moves()
