from odoo import fields, models, api

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    api_origin = fields.Char('API Origin')
    sales_vat_required = fields.Boolean('Sales VAT Required')