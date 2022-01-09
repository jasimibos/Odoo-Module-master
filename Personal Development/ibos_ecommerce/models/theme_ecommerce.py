from odoo import models, fields


class ProductInherited(models.Model):
    _inherit = "product.public.category"
    hot_deals = fields.Boolean(string="Hot Sale", default=False)
