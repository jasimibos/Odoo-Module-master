from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    barcode = fields.Char(string='Contact ID', track_visibility='always', groups="base.group_user")
    is_advance_payment_adjustment = fields.Boolean(string='Is Advance Payment Adjustment', track_visibility='always')
    payment_adjustment_accounting_head = fields.Many2one('account.account', string='Payment Adjustment Head', readonly=True, track_visibility='always')

    @api.model
    def create(self, vals):
        res = super(HrEmployee, self).create(vals)
        if vals.get('is_advance_payment_adjustment'):
            account_types = self.env['account.account.type'].search([('name', '=', 'Payable')])
            account_group = self.env['account.group'].search([('code_prefix', '=', 'empadv')])

            if not account_group:
                account_group = self.env['account.group'].create({
                    'name': 'Employee Advance Payment',
                    'code_prefix': 'empadv'
                })

            account_account = self.env['account.account'].create({
                'code': '71100' + str(res.id),
                'name': 'Advance to ' + vals.get('name'),
                'user_type_id': account_types.id,
                'group_id': account_group.id,
                'reconcile': True
            })
            res.update({
                'payment_adjustment_accounting_head': account_account.id
            })
        return res
    
    def write(self, vals):
        employee = self.env['hr.employee'].search([('id', '=', self.id)])
        if vals.get('is_advance_payment_adjustment') and not employee.payment_adjustment_accounting_head:
            account_types = self.env['account.account.type'].search([('name', '=', 'Payable')])

            account_group = self.env['account.group'].search([('code_prefix', '=', 'empadv')])

            if not account_group:
                account_group = self.env['account.group'].create({
                    'name': 'Employee Advance Payment',
                    'code_prefix': 'empadv'
                })

            account_account = self.env['account.account'].create({
                'code': '71100' + str(self.id),
                'name': 'Advance to ' + employee.name,
                'user_type_id': account_types.id,
                'group_id': account_group.id,
                'reconcile': True
            })
            self.update({
                'payment_adjustment_accounting_head': account_account.id
            })
        return super(HrEmployee, self).write(vals)

    # def contact_id_to_customer_name(self):
    #     employee = self.env['hr.employee'].search([])
    #
    #     for emp in employee:
    #         if emp.barcode:
    #             customer = self.env['res.partner'].search([('id', '=', emp.customer_id.id)])
    #             customer.update({
    #                 'name': customer.name + " (" + emp.barcode + ")"
    #             })