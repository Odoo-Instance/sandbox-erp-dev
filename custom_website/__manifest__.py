# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Custom Coupon",
    'summary': "Use discount coupons in different sales channels.",
    'description': """Integrate coupon mechanism in orders.""",
    'category': 'Sales',
    'version': '1.0',
    'depends': ['account', 'coupon', 'sale_coupon'],
    'data': [
        'views/coupon_program_views.xml',
    ],
    'demo': [
        
    ],
    'installable': True,
    'license': 'LGPL-3',
}