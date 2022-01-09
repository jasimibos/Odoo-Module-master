from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        current_payment = 0
        for aml in res.line_ids:
            current_payment += round(aml.credit, 2)

        account_move = self.env['account.move'].search([('invoice_origin', '=', res.invoice_origin), ('state', '=', 'posted')])
        purchase_order = self.env['purchase.order'].search([('name', '=', res.invoice_origin)])

        total_due_amount = 0
        for am in account_move:
            total_due_amount += am.amount_residual_signed

        total_due_amount = abs(total_due_amount) - abs(current_payment)
        if total_due_amount > 0 or total_due_amount < 0:
            purchase_order.update({
                'payment_status': 'to_payment'
            })
        elif total_due_amount == 0:
            purchase_order.update({
                'payment_status': 'paid'
            })
        return res

    # def write(self, vals):
    #     res = super(AccountMove, self).write(vals)
    #
    #     account_move = self.env['account.move'].search([('invoice_origin', '=', self.invoice_origin)])
    #     full_invoice_payment_state = True
    #     for am in account_move:
    #         if am.invoice_payment_state != 'paid':
    #             full_invoice_payment_state = False
    #
    #     purchase_order = self.env['purchase.order'].search([('name', '=', self.invoice_origin)])
    #     if full_invoice_payment_state:
    #         purchase_order.update({
    #             'payment_status': 'paid'
    #         })
    #
    #     return res
