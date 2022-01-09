from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        validation = self.env['ir.config_parameter'].sudo().get_param('ibos_purchase_management.quantity_validation')
        if validation:
            stoct_picking = self.move_line_ids_without_package.read()
            product_qty_list_count = 0  # count recod for product_qty
            qty_done_list_count = 0  # count recod for qty_done
            is_product_qty_zero = False

            for ord in stoct_picking:
                # print('stoct_picking is ', ord)
                if ord['product_qty'] > 0.0:
                    product_qty_list_count = product_qty_list_count + 1
                else:
                    qty_done_list_count = qty_done_list_count + 1
                if (ord['product_qty'] == 0.0):
                    is_product_qty_zero = True

            if is_product_qty_zero:
                for i in range(product_qty_list_count):
                    for j in range(qty_done_list_count):
                        if stoct_picking[i]['move_id'] == stoct_picking[product_qty_list_count + j]['move_id'] and \
                                stoct_picking[product_qty_list_count + j]['qty_done'] > stoct_picking[i]['product_qty']:
                            raise ValidationError('Done quantity is above order quantity')
            else:
                for ord in stoct_picking:
                    if ord['qty_done'] > ord['product_qty']:
                        raise ValidationError('Done quantity is above order quantity')

        picking = super(StockPicking, self).button_validate()
        return picking

    def action_assign_to_done(self):
        res_ids = self.move_ids_without_package

        for res in res_ids:

            if not res.move_line_nosuggest_ids:
                self.env['stock.move.line'].create({
                    'move_id': res.id,
                    'picking_id': res.picking_id.id,
                    'product_uom_qty': 0.0,
                    'qty_done': res.product_uom_qty,
                    'product_id': res.product_id.id,
                    'product_uom_id': res.product_uom.id,
                    'location_id': res.location_id.id,
                    'location_dest_id': res.location_dest_id.id,
                })

