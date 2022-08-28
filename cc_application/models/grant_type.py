# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

from odoo import api,fields , models , _

class GrantType(models.Model):
    _name = 'grant.types'
    _description = 'Grant Types'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Project Description")
    location_ids = fields.Many2many('cc.location', string="Locations", compute='_compute_location_ids', store=True)
    grant_location_ids = fields.One2many('cc.grant.location', 'grant_type_id', string='Grant Locations')
    website_section_ids = fields.Many2many('website.section')

    round_ids = fields.One2many('cc.round', 'grant_type_id', string='Round')

    @api.depends('grant_location_ids', 'grant_location_ids.location_id')
    def _compute_location_ids(self):
        for record in self:
            record.location_ids = [(6, 0, record.grant_location_ids.mapped('location_id').ids)]

class CcRound(models.Model):
    _name = 'cc.round'
    _description = 'Rounds'

    grant_type_id = fields.Many2one('grant.types', string="Grant Type")
    name = fields.Char(string="Name", required=True)
    grant_location_ids = fields.Many2many(related='grant_type_id.location_ids', store=False, string="Grant Locations")
    location_ids = fields.Many2many('cc.location', string="Locations", domain="[('id', 'in', grant_location_ids)]")
    startdate = fields.Date("Start date")
    enddate = fields.Date("End Date")
