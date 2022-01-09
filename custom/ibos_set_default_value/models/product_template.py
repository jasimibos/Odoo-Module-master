# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Products(models.Model):
    _inherit = "product.template"

    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="Tracking", required=True)

    available_in_pos = fields.Boolean(string='Available in POS')

    def default_get(self, fields):
        value = super(Products, self).default_get(fields)
        value['tracking'] = "lot"
        value['available_in_pos'] = True
        return value
