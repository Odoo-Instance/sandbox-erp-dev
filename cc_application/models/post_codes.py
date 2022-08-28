# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

from odoo import api,fields , models , _

class PostCodes(models.Model):
    _name = 'post.codes'
    
    grant_types_id = fields.Many2one('grant.types', string="Grant Types")    
    cc_postcodes_ids = fields.Many2many('cc.postcodes', string="CC Postcodes")
    