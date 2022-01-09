# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    removal_strategy_id = fields.Many2one('product.removal', 'Force Removal Strategy')
    property_cost_method = fields.Selection([
        ('standard', 'Standard Price'),
        ('fifo', 'First In First Out (FIFO)'),
        ('average', 'Average Cost (AVCO)')], string="Costing Method",
        company_dependent=True, copy=True, required=True)

    property_valuation = fields.Selection([
        ('manual_periodic', 'Manual'),
        ('real_time', 'Automated')], string='Inventory Valuation',
        company_dependent=True, copy=True, required=True)

    def default_get(self, fields):
        value = super(ProductCategory, self).default_get(fields)
        product_rem = self.env['product.removal'].search([('method', '=', 'fifo')])
        value['removal_strategy_id'] = product_rem
        value['property_cost_method'] = "average"
        value['property_valuation'] = "real_time"
        return value

