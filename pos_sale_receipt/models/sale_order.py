# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import Store

from traitlets import default
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    remaning_receipts_count = fields.Integer('Remaning number of receipts', default=0)
    show_warning = fields.Boolean(string="Show Warning", default=False, store=True)
    sale_reference = fields.Char(string='Sale Reference', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        vals['show_warning'] = False
        crm_team_record =  self.env['crm.team'].search([('id', '=', vals['team_id'])])
        if crm_team_record:
            if crm_team_record.ending_sequence_number <= crm_team_record.current_sequence_number:
                raise ValidationError(_('Receipt number exceed threshold sequence number.'))
            if crm_team_record.sales_team_prefix:
                if crm_team_record.ending_sequence_number > crm_team_record.current_sequence_number:
                    crm_team_record.current_sequence_number += 1
                    vals['sale_reference'] = crm_team_record.sales_team_prefix +str(crm_team_record.current_sequence_number)
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
                self.remaning_receipts_count = crm_team_record.ending_sequence_number - crm_team_record.current_sequence_number - 1
                return
        self.show_warning = False
        return
