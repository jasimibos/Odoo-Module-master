from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    res_business_unit_id = fields.Many2one('res.partner.business.unit', string="Partner Business Unit")