from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CreditDeductionLine(models.TransientModel):
    _name = "customer.credit.deduction.line"

    partner_id = fields.Many2one('res.partner', string='Customer')
    phone = fields.Char(related='partner_id.phone', store=True, string="Phone")
    limit = fields.Float(string='Limit')
    credit = fields.Float(string="Credit", store=True,)
    remaining = fields.Float(string='Remaining')
    amount = fields.Float(string="Payment")
    employess_id = fields.Many2one('hr.employee', related='partner_id.employess_id')
    department_id = fields.Many2one('hr.department', related='partner_id.employess_id.department_id', store=True)
    user_id = fields.Many2one('res.users', string='User')
    is_payment_line_status = fields.Boolean(string='Payment Status')

    @api.onchange("amount")
    def _onchange_employee_id(self):
        if self.amount > self.credit:
            raise UserError(_("You can't input Amount more than Credit"))
