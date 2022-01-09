from odoo import fields, models, api

class HrEmployeePublic(models.Model):
    _inherit = 'hr.employee.public'
    barcode = fields.Char(string='Contact ID')
    credit_limit = fields.Float(string="Credit Limit", default=0.0, track_visibility='always')