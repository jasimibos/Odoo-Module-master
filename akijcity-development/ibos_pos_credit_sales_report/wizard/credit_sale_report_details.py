from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date
from datetime import datetime


class CreditDetails(models.TransientModel):
    _name = 'pos.credit.sale.details.wizard'
    _description = 'Point of Sale Credit Sales Details Report'

    start_date = fields.Datetime(required=True, default=fields.Datetime.now())
    end_date = fields.Datetime(required=True, default=fields.Datetime.now())
    customer = fields.Many2many('res.partner', string="Customer", help="List of Customer and Vendors")

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date


    def generate_report(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'customer_ids': self.customer.ids}
        return self.env.ref('ibos_pos_credit_sales_report.credit_sale_details_report').report_action([], data=data)

    def generate_xlsx_report(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'customer_ids': self.customer.ids}
        return self.env.ref('ibos_pos_credit_sales_report.credit_sale_report_xlsx').report_action([], data=data)