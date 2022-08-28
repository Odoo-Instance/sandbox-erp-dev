from odoo import api,fields , models , _

class WebsiteSection(models.Model):
    _name = 'website.section'
    _description = 'Sections'
    _order = 'sequence,id'

    sequence = fields.Integer()
    name = fields.Char(string="Name", required=True)
