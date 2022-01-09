from odoo import fields, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    restrict_discount_control = fields.Boolean(string="Discount Control")