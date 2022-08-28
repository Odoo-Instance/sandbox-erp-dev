from odoo import fields, models


class CCOrgType(models.Model):
    _name = 'cc.org.type'
    _description = 'CC Organisation Type'

    name = fields.Char(string='Organisation Type', required=True)

