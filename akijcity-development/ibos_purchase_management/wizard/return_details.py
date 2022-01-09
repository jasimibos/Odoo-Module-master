# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date
from datetime import datetime


class PosDetails(models.TransientModel):
    _name = 'purchase.return.details.wizard'
    _description = 'Point of Sale Details Report'

    start_date = fields.Datetime(required=True, default=fields.Datetime.now())
    end_date = fields.Datetime(required=True, default=fields.Datetime.now())
    customer_vendor = fields.Many2many('res.partner','purchase_return_vendor', string="Vendor", help="List of Customer and Vendors")

    @api.onchange('start_date')
    def _onchange_start_date(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = self.start_date

    @api.onchange('end_date')
    def _onchange_end_date(self):
        if self.end_date and self.end_date < self.start_date:
            self.start_date = self.end_date

    def generate_report(self):
        data = {'date_start': self.start_date, 'date_stop': self.end_date, 'vendor_ids': self.customer_vendor.ids}
        return self.env.ref('ibos_purchase_management.purchase_return_report').report_action([], data=data)
