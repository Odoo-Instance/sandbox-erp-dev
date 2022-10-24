# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    starting_sequence_number = fields.Integer(string='Starting Sequence number')
    current_sequence_number = fields.Integer(string='Current Sequence number')
    ending_sequence_number = fields.Integer(string='Ending Sequence number')
    sales_team_prefix = fields.Char(string='Sales Team Prefix for sequence', size=3)
    threshold_sequence_number = fields.Integer(string='Threshold Sequence number')

    _sql_constraints = [
    ('sales_team_prefix_uniq', 'unique (sales_team_prefix)',
        " A sales team already exists with same prefix. Please choose another prefix.")
    ]
    




