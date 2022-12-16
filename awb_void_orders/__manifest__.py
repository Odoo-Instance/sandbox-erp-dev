# -*- coding: utf-8 -*-

{
    'name': """Void POS orders""",
    'summary': '''cancel POS orders''',
    'version': '15.0.1.0.1',
    'category': 'Point of sale',
    'website': "http://www.achievewithoutborders.com",
    'author': 'Achieve Without Borders, Inc',
    'license': 'LGPL-3',

    'depends': ['base', 'point_of_sale',],

    'data': [
            'security/ir.model.access.csv',
            'wizard/void_popup.xml',
            'views/pos_orders.xml',
            'views/pos_config.xml',
            
    ],

    'currency': 'EUR',

    'application': True,
    'auto_install': False,
    'installable': True,
}
