from odoo import fields, models, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    list_price = fields.Float("Sales Price", related="product_id.list_price", stored=True, readonly=False)
    mrp_unit = fields.Float("MRP", stored=True, readonly=False)
    price_unit = fields.Float("Unit Price", compute="_compute_unit_mrp_price", stored=True)
    price_cogs = fields.Float("COGS", related="product_id.standard_price", stored=True)

    @api.depends("price_unit")
    def _compute_unit_mrp_price(self):
        for stock in self:
            purchase_order = self.env['purchase.order'].search([('name', '=', stock.origin)])
            purchase_order_line = self.env['purchase.order.line'].search([('product_id', '=', stock.product_id.id), ('order_id', '=', purchase_order.id)])
            stock.price_unit = purchase_order_line.price_unit

    @api.onchange('mrp_unit')
    def _lot_based_on_unit_mrp_price(self):
        stock_production_lot = self.env['stock.production.lot'].search([('product_id', '=', self.product_id.id), ('cost_price', '=', self.price_unit), ('mrp_unit', '=', self.mrp_unit)])
        print("stock_production_lot:", stock_production_lot)
        if stock_production_lot:
            self.lot_id = stock_production_lot[0].id
        else:
            self.lot_id = False
