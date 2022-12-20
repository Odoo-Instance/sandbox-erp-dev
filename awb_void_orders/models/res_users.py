# -*- coding: utf-8 -*-
"""imports from odoo lib"""
from odoo import api, fields, models,_
from odoo.exceptions import UserError

"""inherited model res.users to add a field"""
class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_security_pin = fields.Char(string='Security PIN', size=32, help='A Security PIN used to protect sensible functionality in the Point of Sale')

    @api.constrains('pos_security_pin')
    def _check_pin(self):
        """checking pos pwd pin is digits"""
        if self.pos_security_pin and not self.pos_security_pin.isdigit():
            raise UserError(_("Security PIN can only contain digits"))
