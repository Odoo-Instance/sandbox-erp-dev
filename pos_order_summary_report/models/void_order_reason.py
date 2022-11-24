# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class VoidOrderReason(models.Model):
    _name = 'void.order.reason'

    name = fields.Char('Reason to void order', required=True)
