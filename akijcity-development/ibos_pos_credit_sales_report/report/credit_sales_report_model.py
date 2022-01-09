import logging
from datetime import timedelta
from functools import partial

import psycopg2
import pytz

from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
from odoo.http import request
from odoo.osv.expression import AND
import base64
from datetime import datetime
import collections

_logger = logging.getLogger(__name__)


class ReportSaleDetails(models.AbstractModel):
    _name = "report.ibos_pos_credit_sales_report.credit_sale"
    _description = 'Point of Sale Details'

    def get_credit_details(self, date_start=False, date_stop=False, customer_ids=False, configs=False, session_ids=False):

        branch_name = configs.branch_id.name
        date_start_format = fields.Datetime.from_string(date_start).date()
        date_end_format = fields.Datetime.from_string(date_stop).date()

        data = []
        total_credit_limit = 0.0
        total_credit_consumed = 0.0
        total_credit_remaining = 0.0
        i = 1

        if date_stop:
            date_stop = fields.Datetime.from_string(date_stop).replace(hour=23, minute=59, second=59)
        else:
            date_stop = date_start + timedelta(days=1, seconds=-1)


        customer = self.env['res.partner'].search([])
        for cus in customer:
            pos_order = self.env['pos.order'].search([('partner_id', '=', cus.id), ('date_order', '<=', fields.Datetime.to_string(date_stop))])
            due_amt = 0
            for pos_ord in pos_order:
                due_amt += pos_ord.amount_due

            credit_limit = cus.employess_id.credit_limit
            credit_consumed = round(due_amt, 2)
            credit_remaining = round(credit_limit - credit_consumed, 2)
            phone = cus.employess_id.work_phone
            employee_contruct_id = cus.employess_id.barcode
            total_credit_limit = total_credit_limit + credit_limit
            total_credit_consumed = total_credit_consumed + credit_consumed
            total_credit_remaining = total_credit_remaining + credit_remaining

            if due_amt > 0:
                data.append({
                    'SL': i,
                    'name': cus['name'],
                    'phone': phone,
                    'credit_limit': credit_limit,
                    'credit_consumed': credit_consumed,
                    'credit_remaining': credit_remaining,
                    'contact_id': employee_contruct_id
                })
                i = i + 1

        return {
            'date_start': date_start_format,
            'date_end': date_end_format,
            'current_date': fields.Datetime.now(),
            'data': data,
            'branch_name': branch_name,
            'total_credit': round(total_credit_consumed, 2),
            'total_limit': round(total_credit_limit, 2),
            'total_remainder': round(total_credit_remaining, 2)
        }

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        customers = self.env['res.partner'].browse(data['customer_id'])
        configs = self.env['pos.config'].search([])
        data.update(self.get_credit_details(data['date_start'], data['date_stop'], customers.ids, configs))
        return data
