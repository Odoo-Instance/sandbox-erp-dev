# -*- coding: utf-8 -*-
{
    'name': "pos_order_summary_report",

    'summary': """
        POS Order B3 report""",

    'description': """
        POS Order B3 report
    """,

    'author': "Bhavita Bhatt",
    'category': 'Uncategorized',
    'version': '15.0.1',
    'depends': ['base', 'cc_custom_account', 'sale', 'account_accountant', 'pos_sale_receipt', 'sh_pos_customer_discount', 'point_of_sale'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/pos_order_report_view.xml',
        'views/void_order_reason_view.xml',
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'pos_order_summary_report/static/src/js/model.js',
            'pos_order_summary_report/static/src/js/PopUps/VoidOrderPopups.js',
            'pos_order_summary_report/static/src/js/PopUps/VoidOrderReasonPopup.js',
            'pos_order_summary_report/static/src/js/Screens/ReceiptScreen.js',
            'pos_order_summary_report/static/src/js/Screens/PaymentScreen.js'
        ],

        'web.assets_qweb': [
            'pos_order_summary_report/static/src/xml/ReceiptScreen.xml',
            'pos_order_summary_report/static/src/xml/VoidOrderPopup.xml',
            'pos_order_summary_report/static/src/xml/VoidOrderReasonPopup.xml',
        ],

    },

}
