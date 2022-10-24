# -*- coding: utf-8 -*-
{
    'name': "pos_sale_receipt",

    'summary': """
        AWB POS & sale receipt """,

    'description': """
        Extension Odoo Apps
    """,

    'author': "Achieve Without Borders",

    'category': 'Localization',
    'version': '15.0',

    'depends': ['base', 'point_of_sale', 'sale_management'],

    'data': [
        # 'wizard/sale_order_warning_views.xml',
        'views/crm_team_views.xml',
        'views/sale_order_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pos_sale_receipt/static/src/js/model.js',
            'pos_sale_receipt/static/src/js/sale_order_form_view.js',
        ],
    },
}
