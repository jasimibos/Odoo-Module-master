from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    show_product_qty = fields.Boolean("Show Product Qty", help="Show product qty in pos", default=True)
    default_location_src_id = fields.Many2one("stock.location", related="picking_type_id.default_location_src_id")
    allow_order_out_of_stock = fields.Boolean("Allow order when product out of stock", help="Allow order when location has no product", default=True)