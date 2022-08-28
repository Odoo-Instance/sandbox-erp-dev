from odoo import api,fields , models , _

class CCHeadlineOutputs(models.Model):
    _name = 'cc.headline.outputs'
    _description = 'CC Headline Outputs'

    grant_application_id = fields.Many2one('grant.application', string='Grant Application')
    location_id = fields.Many2one('cc.location', string='Locations')
    name = fields.Char(string='Name', required=True)
    is_headline = fields.Boolean(string='Is Headline')
    headline_text = fields.Float(string='Number')
