# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

from odoo import api,fields , models , _

class CcPostcodes(models.Model):
    _name = 'cc.postcodes'
    _description = 'Postcodes'

    name = fields.Char(string="Name", required=True)
    location_id = fields.Many2one('cc.location')
    
    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'The Post Code name must be unique.'),
    ]