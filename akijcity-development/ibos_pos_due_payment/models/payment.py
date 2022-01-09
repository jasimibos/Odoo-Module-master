from odoo import api, fields, models, _
from odoo.exceptions import UserError

class Pyament(models.Model):
    _name = "due.cutoff.payment"

    partner_id = fields.Many2one('res.partner', string='Customer')
    phone = fields.Char(related='partner_id.phone', store=True, string="Phone")
    limit = fields.Float(string='Limit')
    credit = fields.Float(string="Credit")
    remaining = fields.Float(string='Remaining')
    amount = fields.Integer(string="Amount")
    employess_id = fields.Many2one('hr.employee', related='partner_id.employess_id')

    @api.onchange("amount")
    def _onchange_employee_id(self):
        if self.amount > self.credit:
            raise UserError(_("You can't input Amount more than Credit"))
