from odoo import fields, models, api, _


class AccountTax(models.Model):

	_inherit = 'account.tax'

	tax_type = fields.Selection([('vatable', 'VATABLE'), ('vat_exempt', 'VAT EXEMPT'), ('zero_rated', 'ZERO RATED')], string="Tax Type")