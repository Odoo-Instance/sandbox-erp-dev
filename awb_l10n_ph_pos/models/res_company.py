from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    awb_pos_provider_id = fields.Many2one('res.partner', string='POS Provider')
    awb_pos_provider_street = fields.Char('POS Provider Street')
    awb_pos_provider_street2 = fields.Char('POS Provider Street 2')
    awb_pos_provider_state_id = fields.Many2one('res.country.state', string='POS Provider State')
    awb_pos_provider_country_id = fields.Many2one('res.country', string='POS Provider Country')
    awb_pos_provider_tin = fields.Char('POS Provider TIN')
    awb_pos_provider_accreditation_no = fields.Char('POS Provider Accreditation No.')
    awb_pos_provider_date = fields.Date('POS Provider Date')
    awb_pos_provider_valid_until = fields.Date('POS Provider Valid Until')
    awb_pos_provider_ptu= fields.Char('POS Provider PTU')
    awb_pos_provider_remarks= fields.Text('POS Provider Remarks')
    awb_pos_provider_display_address = fields.Char(compute='_compute_awb_pos_provider_display_address', string='POS Provider Address')
    awb_pos_provider_display_date = fields.Char(compute='_compute_awb_pos_provider_display_date', string='Provider Display Date')
    awb_pos_provider_display_valid_until = fields.Char(compute='_compute_awb_pos_provider_display_date', string='Provider Display Date')
    
    @api.depends('awb_pos_provider_date', 'awb_pos_provider_valid_until')
    def _compute_awb_pos_provider_display_date(self):
        """
            We need this to reformat the default date format 'YYYY-MM-DD' displayed in the POS Order Receipt
            The display format generated in this compute functions is 'MM-DD-YYYY'
        """
        for record in self:
            record.awb_pos_provider_display_date = record.awb_pos_provider_date.strftime('%m/%d/%Y') if record.awb_pos_provider_date else ''
            record.awb_pos_provider_display_valid_until = record.awb_pos_provider_valid_until.strftime('%m/%d/%Y') if record.awb_pos_provider_valid_until else ''

    
    @api.depends('awb_pos_provider_street', 'awb_pos_provider_street2', 'awb_pos_provider_state_id', 'awb_pos_provider_country_id')
    def _compute_awb_pos_provider_display_address(self):
        for record in self:
            record.awb_pos_provider_display_address = ''
            _display_address = ''            
            _display_address += self.awb_pos_provider_street if self.awb_pos_provider_street else ''
            _display_address += f', {self.awb_pos_provider_street2}' if (_display_address and self.awb_pos_provider_street2) else (self.awb_pos_provider_street2 or '')
            _display_address += f', {self.awb_pos_provider_state_id.name}' if (_display_address and self.awb_pos_provider_state_id.name) else (self.awb_pos_provider_state_id.name or '')
            _display_address += f', {self.awb_pos_provider_country_id.name}' if (_display_address and self.awb_pos_provider_country_id.name) else (self.awb_pos_provider_country_id.name or '')
            record.awb_pos_provider_display_address = _display_address

