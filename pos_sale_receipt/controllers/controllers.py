# -*- coding: utf-8 -*-
# from odoo import http


# class PosSaleReceipt(http.Controller):
#     @http.route('/pos_sale_receipt/pos_sale_receipt', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_sale_receipt/pos_sale_receipt/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_sale_receipt.listing', {
#             'root': '/pos_sale_receipt/pos_sale_receipt',
#             'objects': http.request.env['pos_sale_receipt.pos_sale_receipt'].search([]),
#         })

#     @http.route('/pos_sale_receipt/pos_sale_receipt/objects/<model("pos_sale_receipt.pos_sale_receipt"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_sale_receipt.object', {
#             'object': obj
#         })
