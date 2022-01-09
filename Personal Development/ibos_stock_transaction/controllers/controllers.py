# -*- coding: utf-8 -*-
# from odoo import http


# class IbosStockTransaction(http.Controller):
#     @http.route('/ibos_stock_transaction/ibos_stock_transaction/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ibos_stock_transaction/ibos_stock_transaction/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ibos_stock_transaction.listing', {
#             'root': '/ibos_stock_transaction/ibos_stock_transaction',
#             'objects': http.request.env['ibos_stock_transaction.ibos_stock_transaction'].search([]),
#         })

#     @http.route('/ibos_stock_transaction/ibos_stock_transaction/objects/<model("ibos_stock_transaction.ibos_stock_transaction"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ibos_stock_transaction.object', {
#             'object': obj
#         })
