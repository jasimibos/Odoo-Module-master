# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductVarients(models.Model):
    _inherit = "product.product"

    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product')], string='Product Type', required=True, default='product')

    available_in_pos = fields.Boolean(string='Available in POS', default=True)

    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking", required=True, default='lot')


