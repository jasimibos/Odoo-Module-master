from odoo import http
from odoo.http import request


class WebsiteProduct(http.Controller):
    @http.route('/get_product_tab', auth="public", type='json', website=True)
    def get_product_tab(self):

        return "Hussain Ahmed"
