from odoo import fields, models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    stock_alert_qty = fields.Float('Stock Alert Quantity', related='product_tmpl_id.stock_alert_qty',
                                   digits='Product Unit of Measure', default=0)
    # is_low_stock_alert = fields.Boolean(compute='_get_is_low_stock_alert', string='Low Stock Alert', compute_sudo=True,
    #                                     store=True)

    # @api.depends('qty_available', 'stock_alert_qty')
    # def _get_is_low_stock_alert(self):
    #     for low_stock in self:
    #         low_stock.is_low_stock_alert = low_stock.qty_available <= low_stock.stock_alert_qty

