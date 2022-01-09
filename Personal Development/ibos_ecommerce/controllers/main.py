from odoo import http
from odoo.http import request


class slider(http.Controller):
    @http.route('/', auth="public", website=True)
    def index(self, **kw):
        Slider = http.request.env['image.slider']
        Product = http.request.env['product.template']
        category1 = http.request.env['product.public.category'].sudo().search([('hot_deals', '=', True)], limit=6)
        desk = http.request.env['product.template'].sudo().search([('categ_id', '=', 8)], limit=6)
        furniture = http.request.env['product.template'].sudo().search([('categ_id', '=', 5)], limit=6)

        return http.request.render('ibos_ecommerce.home_page', {
            'slider': Slider.search([]),
            'product': Product.search([]),
            'category1': category1,
            'desk': desk,
            'furniture': furniture,

        })
