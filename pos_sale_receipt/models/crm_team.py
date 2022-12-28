# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
import logging

_logger = logging.getLogger(__name__)


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    starting_sequence_number = fields.Integer(string='Starting Sequence number')
    current_sequence_number = fields.Integer(string='Current Sequence number',
                                             compute='onchange_starting_sequence_number', store=True)
    ending_sequence_number = fields.Integer(string='Ending Sequence number', store=True)
    threshold_sequence_number = fields.Integer(string='Threshold Sequence number')
    sale_team_prefix_id = fields.Many2one(string="Sale Team Prefix", comodel_name='sale.team.prefix', copy=False)

    @api.depends('ending_sequence_number')
    def onchange_ending_sequence_number(self):
        for record in self:
            if record.ending_sequence_number < record.current_sequence_number:
                raise UserError(_('Ending sequence number should be greater than current sequence number.'))

    @api.depends('starting_sequence_number')
    def onchange_starting_sequence_number(self):
        for record in self:
            record.current_sequence_number = record.starting_sequence_number


    # this is for to change of starting_sequence_number
    @api.onchange('awb_pos_provider_is_training_mode')
    def onchange_awb_pos_provider_is_training_mode(self):
        if self.awb_pos_provider_is_training_mode:
            self.sale_team_prefix_id = self.env['sale.team.prefix'].search([('name', '=', 'TES')], limit=1)
            print(self.sale_team_prefix_id, "sale_team_prefix_id")
        else:
            self.sale_team_prefix_id = self.env['sale.team.prefix']

    # def action_pos_order_invoice(self):
    #     if self.awb_pos_provider_is_training_mode:
    #         return super().action_pos_order_invoice()
    #     if not self.env.user.is_admin:
    #         raise AccessError("Only admin users can access this flag")

    # rest of the method implementation goes here
    # def awb_pos_provider_is_training_mode(self):
    #     if not self.env.user.is_admin:
    #         raise AccessError("Only admin users can access this flag")

    # def awb_pos_provider_is_training_mode(self):
    #     if self.env.user.is_admin:
    #         if self.awb_pos_provider_is_training_mode is None:
    #             self.awb_pos_provider_is_training_mode = False
