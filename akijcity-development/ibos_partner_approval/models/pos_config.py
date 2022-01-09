from odoo import fields, models, api

class PosConfig(models.Model):
    _inherit = 'pos.config'

    allow_create_partner = fields.Boolean(string="Allow Create Partner on POS", default=True)