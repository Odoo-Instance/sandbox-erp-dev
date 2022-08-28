# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

from odoo import api,fields , models , _

class Locations(models.Model):
    _name = 'cc.location'
    _description = 'Locations'

    name = fields.Char(string="Name", required=True)
    post_code_ids = fields.One2many('cc.postcodes', 'location_id', string="Post Code")
    strategic_objective_ids = fields.One2many('cc.strategic.objectives', 'location_id', string='Strategic Objectives')
    headline_outputs_ids = fields.One2many('cc.headline.outputs', 'location_id', string='Headline Outputs')
    location_code = fields.Char(string='Location Code', size=2)
    location_sequence = fields.Integer(string='Sequence')
