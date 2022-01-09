from odoo import api, fields, models, _
from . import barcode


class DynamicProductBarcode(models.TransientModel):
    _name = 'dynamic.product.product.barcode.number'

    @api.model
    def default_get(self, fields):
        res = super(DynamicProductBarcode, self).default_get(fields)
        active_ids = self._context.get('active_ids')
        sale_order_ids = self.env['product.product'].browse(active_ids)
        return res

    def dynamic_product_barcode(self):
        self.ensure_one()
        product_ids = self.env['product.product'].browse(self._context.get('active_ids'))

        for prod in product_ids:
            product_id = prod.id
            default_code = product_id
            if prod.to_weight:
                default_code = prod.default_code
                prefix = self.env['ir.config_parameter'].sudo().get_param(
                    'km_dynamic_product_barcode_number.barcode_prefix')
                ean = str(prefix) + '0' * (5 - len(default_code)) + default_code + "000000"
                eanbarcode = ean
            else:
                eanbarcode = barcode.generate_ean(self, str(default_code))

            self.env.cr.execute(
                "update product_product set barcode='" + str(eanbarcode) + "' where id='" + str(product_id) + "'")
