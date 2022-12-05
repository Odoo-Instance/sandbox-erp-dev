# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

<<<<<<< HEAD
# from ast import Store

# from traitlets import default
=======
>>>>>>> develop
from odoo import fields, models, api, _

class SaleTeamPrefix(models.Model):
    _name = "sale.team.prefix"

    name = fields.Char(string='Sales Team Prefix for sequence', size=3, copy=False)

    _sql_constraints = [
    ('sales_team_prefix_uniq', 'unique (name)',
        " A sales team already exists with same prefix. Please choose another prefix.")
    ]
