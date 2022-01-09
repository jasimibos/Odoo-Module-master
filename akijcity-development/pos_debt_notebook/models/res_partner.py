from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Float(string="Credit Limit", track_visibility='always')
