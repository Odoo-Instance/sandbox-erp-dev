# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    taxpayer_min = fields.Char()  # move this
    taxpayer_machine_serial_number = fields.Char()
    awb_pos_provider_ptu = fields.Char('POS Provider PTU')  # move this
    awb_pos_provider_remarks = fields.Text(
        'POS Provider Remarks', readonly=True, compute='_check_if_training_mode')  # move this
    awb_pos_provider_is_training_mode = fields.Boolean(
        help="If you are using this Training mode your journal entries and cash flow will not calculated")  # move this


    @api.depends('awb_pos_provider_is_training_mode')
    def _check_if_training_mode(self):
        for record in self:
            if record.awb_pos_provider_is_training_mode:
                record.awb_pos_provider_remarks = 'THIS IS NOT AN OFFICIAL RECEIPT'
            else:
                record.awb_pos_provider_remarks = 'THIS SERVES AS YOUR OFFICIAL RECEIPT'
