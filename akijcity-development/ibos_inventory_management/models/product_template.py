import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)

class ProductTempale(models.Model):
    _inherit = 'product.template'

    mrp = fields.Float("MRP", store=True)
    show_mrp = fields.Boolean(default=False)

    @api.model
    def default_get(self, fields):
        res = super(ProductTempale, self).default_get(fields)
        product_category_check = self.env['ir.config_parameter'].sudo().get_param(
            'ibos_inventory_management.group_product_category')
        show_mrp_field = self.env['ir.config_parameter'].sudo().get_param(
            'ibos_inventory_management.mrp_inventory_and_purchase')

        default_type_get = self.env['ir.config_parameter'].sudo().get_param('ibos_inventory_management.type')

        if self.categ_id.product_category_ref.id:
            self.pos_categ_id = self.categ_id.product_category_ref.id
        else:
            self.pos_categ_id = False

        if len(res) > 0:
            if product_category_check:
                res['available_in_pos'] = True
            if show_mrp_field:
                res['show_mrp'] = True
            if default_type_get:
                if default_type_get == 'consu':
                    res['type'] = 'consu'
                if default_type_get == 'service':
                    res['type'] = 'service'
                if default_type_get == 'product':
                    res['type'] = 'product'

        return res


