# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrderWarning(models.TransientModel):
    _name = "sale.order.warning"
    _description = "Sales order receipt warning"

    message = fields.Char(string='Only few receipts left')
