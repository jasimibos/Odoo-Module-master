from odoo import api, fields, models, _

class partner(models.Model):
    _inherit = "res.partner"
    _rec_name = 'name'

    employess_id = fields.Many2one("hr.employee", readonly=True)


