from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    employee_id = fields.Many2one('hr.employee', string="Adjustment Employee", track_visibility="always", domain=[('is_advance_payment_adjustment', '=', True)])
    is_advance_adjustment = fields.Boolean(string='Allow Employee Adjustment',  track_visibility="always",)

    @api.model
    def create(self, vals):
        if vals.get("is_advance_adjustment"):
            for line_id in vals.get("line_ids"):
                employee_id = vals.get("employee_id")
                hr_employee = self.env['hr.employee'].search([('id', '=', employee_id)])
                account_id = hr_employee.payment_adjustment_accounting_head.id

                for line in line_id:
                    if 'account_id' in str(line):
                        account_account = self.env['account.account'].search([('id', '=', line.get('account_id'))])

                        if account_account.name == 'Account Payable':
                            line.update({
                                'account_id': account_id
                            })
        return super(AccountMove, self).create(vals)

    def write(self, vals):
        if 'employee_id' in vals:
            for line in self.line_ids:
                hr_employee = self.env['hr.employee'].search([('id', '=', vals.get('employee_id'))])
                if line.account_id.group_id.code_prefix == 'empadv':
                    line.update({
                        'account_id': hr_employee.payment_adjustment_accounting_head.id
                    })
                elif line.account_id.name == 'Account Payable':
                    line.update({
                        'account_id': hr_employee.payment_adjustment_accounting_head.id
                    })
        return super(AccountMove, self).write(vals)