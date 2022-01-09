from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError, AccessError


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    @api.model
    def search_employee_rec(self, customer_id):
        emp = self.env['hr.employee'].search([('id', '=', customer_id[0])])
        order = self.env['pos.order'].search([('partner_id', '=', emp["customer_id"].id)])
        customer_credit_payment_list = self.env['customer.credit.payment.line'].search([('partner_id', '=' , emp["customer_id"].id)])

        total = 0.0
        total_paid = 0.0
        credit_payment = 0.0

        for o in order:
            total += o["amount_total"]
            total_paid += o["amount_paid"]

        for i in customer_credit_payment_list:
            print('customer_credit_payment_list',i.amount)
            credit_payment += i.amount

        total = total + customer_id[2]
        total_paid = total_paid + customer_id[3]
        flag = 0

        if((total - total_paid) - credit_payment <= emp["credit_limit"]):
            flag = 1
            return flag
        else:
            return flag




