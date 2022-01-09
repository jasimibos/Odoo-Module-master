from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'
    plu_no = fields.Integer(string='PLU No')
    default_code = fields.Char(string='Item Code')


