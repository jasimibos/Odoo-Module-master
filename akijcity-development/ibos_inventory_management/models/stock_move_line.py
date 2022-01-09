from odoo import fields, models, api

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    standard_price = fields.Float(string="Cost Price", readonly=True, store=True)
    
    @api.model
    def create(self, vals):
        res = super(StockMoveLine, self).create(vals)
        product_id = self.env['product.product'].search([('id', '=', vals.get('product_id'))])
        res.update({
            'standard_price': product_id.standard_price
        })
        return res

    def write(self, vals):
        product_id = self.env['product.product'].search([('id', '=', self.product_id.id)])
        if product_id:
            vals['standard_price'] = product_id.standard_price
        return super(StockMoveLine, self).write(vals)