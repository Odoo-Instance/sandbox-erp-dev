# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

from odoo import api,fields , models , _
from odoo.exceptions import ValidationError


class CCGrantLocations(models.Model):
    _name = 'cc.grant.location'
    _description = 'CC Grant Locations'
    _rec_name = 'location_id'

    location_id = fields.Many2one('cc.location', string='Location', required=True)
    grant_type_id = fields.Many2one('grant.types', string='Grant Types')
    tier_one = fields.Monetary(string='T1', default=1)
    tier_two = fields.Monetary(string='T2')
    tier_three = fields.Monetary(string='T3')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.id)

    @api.constrains('tier_one', 'tier_two', 'tier_three')
    def _check_tier(self):
        for record in self:
            if record.tier_one <= 0 or record.tier_two <= 0 or record.tier_three <= 0:
                raise ValidationError(_('Tier Value must be greater then zero.'))
            if record.tier_two <= record.tier_one:
                raise ValidationError(_('Tier Two Value must be greater then Tier One.'))
            elif record.tier_three <= record.tier_two:
                raise ValidationError(_('Tier Three Value must be greater then Tier Two.'))
            elif record.tier_three <= record.tier_one:
                raise ValidationError(_('Tier Three Value must be greater then Tier One.'))
