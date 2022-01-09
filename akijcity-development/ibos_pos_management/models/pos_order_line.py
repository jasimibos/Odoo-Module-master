import logging
from datetime import timedelta
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
from odoo.osv.expression import AND
import base64

_logger = logging.getLogger(__name__)

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    mrp = fields.Float(string='MRP', default= 0.0, compute='get_mrp_from_product')

    def get_mrp_from_product(self):
        for line in self:
            if line.product_id.product_tmpl_id.mrp:
                line.mrp = line.product_id.product_tmpl_id.mrp