import logging
from odoo import api, fields, models, tools, _
_logger = logging.getLogger(__name__)

class PosConfig(models.Model):
    _inherit = 'pos.config'

    partial_payment = fields.Boolean("Enable Partial payment", help="Show Credit button", default=False)
