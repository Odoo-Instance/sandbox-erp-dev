# -*- coding: utf-8 -*-


from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    sh_enable_customer_discount = fields.Boolean(
        string='Enable Customer Discount')


class PosOrder(models.Model):
    _inherit = 'res.partner'

    sh_customer_discount = fields.Integer(string='Default POS Discount')
    sc_pwd = fields.Selection([('sc', 'SC'),('pwd', 'PWD')], string='Choose SC/PWD')
    check_sc_pwd = fields.Boolean(string='SC/PWD')
    #check_pwd = fields.Boolean(string='PWD')

    @api.model
    def default_get(self, fields):
        vals = super(PosOrder, self).default_get(fields)
        customer_discount = self.env.user.company_id.sh_customer_discount
        if 'sh_customer_discount' in fields:
            vals['sh_customer_discount'] = customer_discount
        return vals



class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    sh_customer_discount = fields.Char(string="Pos Discount", default='0')


class ResConfigSettingInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    sh_customer_discount = fields.Char(string="Default Pos Discount", related='company_id.sh_customer_discount', readonly=False)
