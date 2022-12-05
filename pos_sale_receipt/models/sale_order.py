# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    show_warning = fields.Boolean(string="Show Warning", default=False, store=True)
    sale_reference = fields.Char(string='Sale Reference', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        vals['show_warning'] = False
        crm_team_record =  self.env['crm.team'].search([('id', '=', vals['team_id'])])
        if crm_team_record:
            if crm_team_record.ending_sequence_number <= crm_team_record.current_sequence_number:
                raise ValidationError(_('Receipt number reached threshold sequence number.'))
            if crm_team_record.sale_team_prefix_id:
                if crm_team_record.ending_sequence_number > crm_team_record.current_sequence_number:
                    crm_team_record.current_sequence_number += 1
                    current_sequence_number_with_format = str(crm_team_record.current_sequence_number).zfill(6)
                    if crm_team_record.ending_sequence_number > pow(9,6):
                        length_of_ending_sequence_number = len(str(crm_team_record.ending_sequence_number))
                        current_sequence_number_with_format = str(crm_team_record.current_sequence_number).zfill(length_of_ending_sequence_number)
                    vals['sale_reference'] = crm_team_record.sale_team_prefix_id.name + ' ' + str(current_sequence_number_with_format)
                if crm_team_record.threshold_sequence_number < crm_team_record.current_sequence_number:
                    vals['show_warning'] = True
            else:
                raise ValidationError(_('Please add sales prefix in Sales Team'))
        return super().create(vals)


    @api.onchange('team_id')
    def _onchange_user_team_id(self):
        crm_team_record =  self.env['crm.team'].search([('id', '=', self.team_id.id)])
        if crm_team_record:
            if crm_team_record.threshold_sequence_number < crm_team_record.current_sequence_number:
                self.show_warning = True
                return
        self.show_warning = False
        return

    def _create_invoices(self, grouped=False, final=False, date=None):
        moves = super()._create_invoices(grouped=grouped, final=final, date=date)
        for move in moves:
            move['sale_order_id'] = self.id
        return moves