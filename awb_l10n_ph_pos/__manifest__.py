# -*- coding: utf-8 -*-
{
    'name': "AWB Philippine Point of Sale Localization",

    'summary': "AWB Philippine Point of Sale Localization",

    'description': """
        AWB Philippine Point of Sale Localization
    """,

    'author': "Achieve Without Borders, Inc.",
    'website': "https://www.achievewithoutborders.com/page/odoo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '15.0.7.1',

    # any module necessary for this one to work correctly
    'depends': [
        'point_of_sale',
        'point_of_sale.models',
    ],

    # always loaded
    'data': [
        'views/res_company.xml',
    ],

    'assets': {
        'web.assets_qweb': [
            'awb_l10n_ph_pos/static/src/xml/pos_receipt.xml',
        ],
        'web.assets_backend': [
            'awb_l10n_ph_pos/static/src/js/pos_receipt.js',
            'awb_l10n_ph_pos/static/src/js/models.js',
        ],
    },
}
