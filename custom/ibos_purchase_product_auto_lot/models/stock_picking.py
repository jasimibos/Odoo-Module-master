from odoo import fields, models, api
import uuid

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_set_quantities_to_reservation(self):
        for move in self:
            for move_line in move.move_line_ids:
                if move.has_tracking != 'none':
                    lot_name = uuid.uuid4()
                    lot_id = self.env['stock.production.lot'].create({
                        'company_id': self.env.company.id, 'product_id': move_line.product_id.id,
                        'name': lot_name, 'lot_name': lot_name, 'list_price': move_line.list_price,
                        'warehouse_id': move.warehouse_id.id, 'list_price': move_line.list_price, 'last_sales_price': 0, 'mrp_unit': move_line.mrp_unit, 'cost_price': move_line.price_unit})
                    move_line.update({'lot_id': lot_id})

        return super(StockPicking, self).action_set_quantities_to_reservation()