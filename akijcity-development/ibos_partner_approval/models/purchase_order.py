from odoo import fields, models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one('res.partner', domain="[('state', '=', 'approved')]")