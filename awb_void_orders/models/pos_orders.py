# -*- coding: utf-8 -*-
"""imports from odoo lib"""
from odoo import api, fields, models
from odoo.exceptions import UserError

"""Inherited model pos.order"""
class PosOrdersInherit(models.Model):
    _inherit = 'pos.order'
    
    #overide the state field
    state = fields.Selection(
        [('draft', 'New'), ('cancel', 'Cancelled'), ('paid', 'Paid'), ('done', 'Posted'), ('invoiced', 'Invoiced'),('voided', 'Voided')],
        'Status', readonly=True, copy=False, default='draft')
    

"""Inherited model pos.order"""
class AccountMoveInherited(models.Model):
    _inherit = 'account.move'
    _decription = 'void the records'
    
    
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
            ('voided', 'Voided'),
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    
    
    