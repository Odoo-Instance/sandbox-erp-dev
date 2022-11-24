# -*- coding: utf-8 -*-
 

{
    "name": "Point Of Sale Order Customer Discount",
    "author": "Tarun kumar",
    "category": "Point of Sale",
    "license": "OPL-1",
    "summary": "POS Customer Discount, Point Of Sale Customer Discount, Point Of Sale Order Line Customer Discount, POS Custom Discount,Point Of Sale Discount,POS Discount, POS Line Discount,Special Customer Discount Odoo",
    "description": """Do you want to add a discount automatically from a customer in the point of sale order? This module helps to apply POS order discount automatically when selecting the customer, so you need to define it only once time then after, it will automatically be added in every order.""",
    "version": "15.0.2",
    "depends": ["point_of_sale"],
    "application": True,
    "data": ['views/pos_config.xml'],
    'assets': {'point_of_sale.assets': ['sh_pos_customer_discount/static/src/js/pos.js',
                                        'sh_pos_customer_discount/static/src/js/pos_buttons.js',
                                        'sh_pos_customer_discount/static/src/js/pos_buttons_pwd.js',
                                        'sh_pos_customer_discount/static/src/js/discount_popup.js'
                                        ],
               'web.assets_qweb': ['sh_pos_customer_discount/static/src/xml/pos.xml',
                                   'sh_pos_customer_discount/static/src/xml/pos_buttons.xml',
                                    'sh_pos_customer_discount/static/src/xml/pos_buttons_pwd.xml',
                                    'sh_pos_customer_discount/static/src/xml/discount_popup.xml'
                                   ],},
    "images": ["static/description/background.png", ],
    "auto_install": False,
    "installable": True,
    "price": 15,
    "currency": "EUR"
}
