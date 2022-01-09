# -*- coding: utf-8 -*-
from odoo import api, fields, models


class OperationsType(models.Model):
    _inherit = "stock.picking.type"

    code = fields.Selection([('incoming', 'Receipt'),
                             ('outgoing', 'Delivery'),
                             ('internal', 'Internal Transfer')],
                            'Type of Operation', required=True)

    show_operations = fields.Boolean('Show Detailed Operations')

    show_reserved = fields.Boolean('Pre-fill Detailed Operations')

    use_create_lots = fields.Boolean('Create New Lots/Serial Numbers')

    use_existing_lots = fields.Boolean('Use Existing Lots/Serial Numbers')

    def default_get(self, fields):
        value = super(OperationsType, self).default_get(fields)
        value['code'] = "incoming"
        value['show_operations'] = True
        value['use_create_lots'] = True
        value['use_existing_lots'] = True
        return value

    @api.model
    def create(self, vals):
        res = super(OperationsType, self).create(vals)
        res['use_existing_lots'] = True
        res['show_operations'] = True
        res['show_reserved'] = True
        return res
