from odoo import api, fields, models, _
import base64
import json
import logging

_logger = logging.getLogger(__name__)


class pos_order(models.Model):
    _inherit = "pos.order"

    ean13 = fields.Char('Ean13')

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(pos_order, self)._order_fields(ui_order)

        if ui_order.get('ean13', False):
            order_fields.update({
                'ean13': ui_order['ean13']
            })

        return order_fields

