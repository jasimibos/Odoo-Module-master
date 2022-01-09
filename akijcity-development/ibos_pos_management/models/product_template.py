import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
import json
from odoo.tools import date_utils
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def get_ordered_products_mrp(self, ordered_product_ids):
        products = self.env['product.template'].search([('id', '=', ordered_product_ids)])
        mrp = []
        for p in products:
            if p.mrp:
                mrp.append({
                    'id': p.id,
                    'mrp': p.mrp
                })
        json_data = json.dumps(mrp, default=date_utils.json_default)
        return mrp
