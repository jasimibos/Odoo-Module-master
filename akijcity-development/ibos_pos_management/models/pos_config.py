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

class PosConfig(models.Model):
    _inherit = 'pos.config'

    show_mrp_on_pos_recipt = fields.Boolean(string='Show MRP on receipt', default=False)