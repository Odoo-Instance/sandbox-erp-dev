# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    starting_sequence_number = fields.Integer(string='Starting Sequence number')
    current_sequence_number = fields.Integer(string='Current Sequence number')
    ending_sequence_number = fields.Integer(string='Ending Sequence number', store=True)
    threshold_sequence_number = fields.Integer(string='Threshold Sequence number')
    sale_team_prefix_id = fields.Many2one(string="Sale Team Prefix", comodel_name='sale.team.prefix', copy=False)

    @api.onchange('ending_sequence_number')
    def onchange_ending_sequence_number(self):
        for record in self:
            if record.ending_sequence_number < record.current_sequence_number:
                raise UserError(_('Ending sequence number should be greater than current sequence number.'))

