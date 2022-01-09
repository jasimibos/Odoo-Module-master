from odoo import api, fields, models, _
from datetime import datetime
from odoo.http import request


class CreditDeduction(models.Model):
    _name = 'customer.credit.deduction'
    _description = 'Point of Sale Details Report'
    _inherit = 'mail.thread'
    # _rec_name = ""

    name = fields.Char(string='Name')
    payment_method = fields.Many2one('pos.payment.method', string='Payment', required=True)
    is_credit_as_payment = fields.Boolean(string="Credit as Payment")
    is_payment_status = fields.Boolean(string="Payment Status")
    credit_customers = fields.Many2many('customer.credit.deduction.line', string='Credit Customers')
    state = fields.Selection([('draft', 'Draft'), ('payment', 'Payment'), ('cancel', 'Cancel')], string='State',
                             default='draft')
    start_date = fields.Date(required=True, default=fields.Datetime.now())
    end_date = fields.Date(required=True, default=fields.Datetime.now())
    payment_date = fields.Date(required=True, default=fields.Datetime.now())

    @api.model
    def default_get(self, field_list):
        res = super(CreditDeduction, self).default_get(field_list)
        res.update({
            'name': 'Deduction Employee Credit of ' + datetime.today().strftime("%b") + " - " + datetime.today().strftime(
                "%Y"),
        })
        return res

    def action_generate_credit_customer(self):
        uid = request.session.uid
        start_date = self.start_date
        end_date = self.end_date
        partners = self.env['res.partner'].sudo().search([])
        user_id = self.env['res.users'].sudo().search([('id', '=', uid)])
        due_user = self.env["customer.credit.deduction.line"].sudo().search([('user_id', '=', user_id.id)])
        due_user.unlink()

        for partner in partners:
            if partner:
                limit = partner.employess_id.credit_limit
                pos_order = self.env['pos.order'].sudo().search([('partner_id', '=', partner.id), ('date_order', '>=', start_date), ('date_order', '<=', end_date)])

                credit = 0
                for ord in pos_order:
                    credit += ord.amount_total - ord.amount_paid
                remaining = limit - credit
            if credit > 0:
                amount = 0
                if self.is_credit_as_payment:
                    amount = credit

                payment_line = self.env["customer.credit.deduction.line"].sudo().create({
                    'partner_id': partner.id,
                    'phone': partner.phone,
                    'limit': limit,
                    'credit': credit,
                    'remaining': remaining,
                    'amount': amount,
                    'user_id': user_id.id,
                })
    @api.onchange("credit_customers")
    def _onchange_employee_id(self):
        for credit_customer in self.credit_customers._origin:
            if credit_customer.id:
                credit_customer.limit = credit_customer.employess_id.credit_limit
                pos_order = self.env['pos.order'].search([('partner_id', '=', credit_customer.id)])
                due = 0
                for ord in pos_order:
                    due += ord.amount_total - ord.amount_paid
                credit_customer._origin.credit = due
                credit_customer._origin.remaining = credit_customer.limit - credit_customer.credit



    def action_make_credit_payment(self):
        amount = 0
        for customer in self.credit_customers:
            customer.update({
                'is_payment_line_status': True
            })

            if customer.amount > 0:
                amount += customer.amount
                self.env["customer.credit.payment.line"].create({
                    'name': self.name,
                    'partner_id': customer.partner_id.id,
                    'phone': customer.partner_id.phone,
                    'limit': customer.limit,
                    'credit': customer.credit,
                    'remaining': customer.remaining,
                    'amount': customer.amount,
                    'current_remaining': customer.credit - customer.amount,
                    'user_id': customer.user_id.id,
                    'payment_date': self.payment_date
                })
                customer.unlink()

        # journal entry
        line = self
        tmpl_id = line.payment_method

        recurr_code = str(tmpl_id.id) + '/' + str(line.payment_date)
        line_ids = [(0, 0, {
            'name': line.name,
            'account_id': tmpl_id.receivable_account_id.id,
            'credit': amount,
        }), (0, 0, {
            'name': line.name,
            'account_id': tmpl_id.cash_journal_id.default_debit_account_id.id,
            'debit': amount,
        })]
        vals = {
            'date': line.payment_date,
            'recurring_ref': recurr_code,
            'company_id': self.env.company.id,
            'journal_id': tmpl_id.cash_journal_id.id,
            'ref': line.name,
            'narration': 'Credit Customer Payment',
            'line_ids': line_ids
        }
        move_id = self.env['account.move'].create(vals)
        move_id.post()

    @api.onchange('is_credit_as_payment')
    def set_credit_as_payment(self):
        for customer in self.credit_customers:
            customer._origin.amount = customer._origin.credit

        if self.is_credit_as_payment:
            pass


    def action_set_customer_due(self):
        date_string = "30-09-2021 23:59:59"
        order_date = datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S")

        domain = [('date_order', '<=', order_date), ('pos_reference', 'not in', ('Order 00043-008-00049', 'Order 00041-020-01293', 'Order 00036-001-00019', 'Order 00035-008-00064', 'Order 00034-007-00266', 'Order 00034-006-00139', 'Order 00034-006-00122', 'Order 00033-016-01112', 'Order 00033-016-01099', 'Order 00033-008-00448', 'Order 00033-005-00119', 'Order 00033-005-00072', 'Order 00032-009-00316', 'Order 00032-008-00296', 'Order 00032-008-00272', 'Order 00032-002-00140', 'Order 00029-015-00177', 'Order 00029-006-00458', 'Order 00027-013-00021', 'Order 00027-002-00049', 'Order 00026-009-01336', 'Order 00026-007-01004', 'Order 00026-005-00607', 'Order 00025-008-00890', 'Order 00025-008-00630', 'Order 00024-007-00313', 'Order 00024-007-00238', 'Order 00023-020-01198','Order 00023-020-01099','Order 00023-015-00692','Order 00022-010-00018','Order 00022-007-00261','Order 00021-001-00017','Order 00019-014-00234','Order 00018-008-00371','Order 00017-021-00616','Order 00016-008-00298','Order 00016-003-00101','Order 00014-041-01539','Order 00014-032-00837'))]
        pos_order = self.env['pos.order'].search(domain, order="id desc")
        for order in pos_order:
            order.write({'amount_due': order.amount_paid})

    # customer_payment = self.env['customer.credit.payment.line'].search([])
        # date_string = "30-09-2021"
        # order_date = datetime.strptime(date_string, "%d-%m-%Y")
        #
        # domain = [('date_order', '<=', order_date)]
        # pos_order = self.env['pos.order'].search(domain, order="id desc")
        # for order in pos_order:
        #     if order.partner_id.id == 564:
        #         print("pos_order:", order.name, order.amount_due, order.partner_id.id)
        #
        # for payment in customer_payment:
        #     payment_amount = payment.amount
        #     domain = [('partner_id', '=', payment.partner_id.id), ('date_order', '<=', order_date), ('pos_reference', 'not in', ('Order 00043-008-00049', 'Order 00041-020-01293', 'Order 00036-001-00019', 'Order 00035-008-00064', 'Order 00034-007-00266', 'Order 00034-006-00139', 'Order 00034-006-00122', 'Order 00033-016-01112', 'Order 00033-016-01099', 'Order 00033-008-00448', 'Order 00033-005-00119', 'Order 00033-005-00072', 'Order 00032-009-00316', 'Order 00032-008-00296', 'Order 00032-008-00272', 'Order 00032-002-00140', 'Order 00029-015-00177', 'Order 00029-006-00458', 'Order 00027-013-00021', 'Order 00027-002-00049', 'Order 00026-009-01336', 'Order 00026-007-01004', 'Order 00026-005-00607', 'Order 00025-008-00890', 'Order 00025-008-00630', 'Order 00024-007-00313', 'Order 00024-007-00238', 'Order 00023-020-01198','Order 00023-020-01099','Order 00023-015-00692','Order 00022-010-00018','Order 00022-007-00261','Order 00021-001-00017','Order 00019-014-00234','Order 00018-008-00371','Order 00017-021-00616','Order 00016-008-00298','Order 00016-003-00101','Order 00014-041-01539','Order 00014-032-00837'))]
        #     pos_order = self.env['pos.order'].search(domain, order="id desc")
        #
        #     for order in pos_order:
        #         order.write({'amount_due': order.amount_paid})


    def action_fix_paid_order(self):
        pos_orders = self.env['pos.order'].search([('amount_paid', '=', 0), ('amount_due', '='
                                                                                           '', 0)])
        for order in pos_orders:
            pos_payments = self.env['pos.payment'].search([('pos_order_id', '=', order.id)])
            total_payment = 0
            for payment in pos_payments:
                total_payment += payment.amount
            order.write({'amount_paid': total_payment})