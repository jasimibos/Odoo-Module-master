from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    lst_price = fields.Float('Sales Price', related='product_id.list_price', store=True, readonly=False)
    profit_margin = fields.Float("Margin (%)", store=True)
    show_lst_price_and_margin = fields.Boolean(default=False)
    mrp = fields.Float("MRP", store=True)
    show_mrp = fields.Boolean(default=False)

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrderLine, self).default_get(fields)
        show_mrp_field = self.env['ir.config_parameter'].sudo().get_param('ibos_inventory_management.mrp_inventory_and_purchase')
        show_sale_and_margin_field = self.env['ir.config_parameter'].sudo().get_param('ibos_purchase_management.sales_prise_and_margin')
        if len(res) > 0:
            if show_mrp_field:
                res['show_mrp'] = True
            if show_sale_and_margin_field:
                res['show_lst_price_and_margin'] = True
        return res

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for order_line in self:
            order_line.update({
                'lst_price': order_line.product_id.lst_price
            })

    @api.onchange('lst_price', 'price_unit')
    def _onchange_profit_margin(self):
        profit_margin = 0
        for order_line in self:
            if self.lst_price > 0:
                profit = self.lst_price - self.price_unit
                profit_margin = (profit/self.lst_price)*100
            order_line.update({
                'profit_margin': profit_margin
            })
