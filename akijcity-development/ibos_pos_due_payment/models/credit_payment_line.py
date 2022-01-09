from odoo import api, fields, models, _
from datetime import date, datetime, time

class CreditPaymentLine(models.Model):
    _name = "customer.credit.payment.line"

    name = fields.Char(string='Name')
    partner_id = fields.Many2one('res.partner', string='Customer')
    phone = fields.Char(related='partner_id.phone', store=True, string="Phone")
    limit = fields.Float(string='Limit')
    credit = fields.Float(string="Credit")
    remaining = fields.Float(string='Remaining')
    amount = fields.Float(string="Payment")
    current_remaining = fields.Float(string="Current Remaining")
    user_id = fields.Many2one('res.users', string='User')
    payment_date = fields.Date(string='Payment Date', default=date.today(), required=True)