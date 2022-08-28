# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

from odoo import api,fields , models , _

class CCStrategicObjectives(models.Model):
    _name = 'cc.strategic.objectives'
    _description = 'CC Strategic Objectives'

    grant_application_id = fields.Many2one('grant.application', string='Grant Application')
    location_id = fields.Many2one('cc.location', string='Locations')
    name = fields.Char(string='Name', required=True)
    is_strategic = fields.Boolean(string='Is Strategic')
    strategic_text = fields.Text(string='Strategic')
