from odoo import http
from odoo.http import request


class ProductController(http.Controller):
    @http.route('product/details', website=True, auth='public')
    def product_details(self, **kw):
        print("Hello")

