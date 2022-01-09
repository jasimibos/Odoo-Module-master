from odoo import models
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


class PartnerXlsx(models.AbstractModel):
    _name = 'report.ibos_pos_credit_sales_report.credit_sale_xlsx'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def get_credit_details(self, date_start=False, date_stop=False, customer_ids=False, configs=False, session_ids=False):

        branch_name = configs.branch_id.name
        date_start_format = fields.Datetime.from_string(date_start).date()
        date_end_format = fields.Datetime.from_string(date_stop).date()

        data = []
        total_credit_limit = 0.0
        total_credit_consumed = 0.0
        total_credit_remaining = 0.0
        total_credit_purchase = 0.0
        total_credit_return = 0.0
        total_paid_amount = 0.0
        i = 1

        if date_start:
            date_start = fields.Datetime.from_string(date_start).replace(hour=0, minute=0, second=0)
        else:
            date_start = date_start + timedelta(days=1, seconds=-1)

        if date_stop:
            date_stop = fields.Datetime.from_string(date_stop).replace(hour=23, minute=59, second=59)
        else:
            date_stop = date_start + timedelta(days=1, seconds=-1)


        domain = []
        if customer_ids:
            domain = [('id', 'in', customer_ids)]
        customer = self.env['res.partner'].search(domain, order="barcode desc")
        for cus in customer:
            pos_order = self.env['pos.order'].search([('partner_id', '=', cus.id), 
                                                      ('date_order', '>=', fields.Datetime.to_string(date_start)),
                                                      ('date_order', '<=', fields.Datetime.to_string(date_stop))])
            due_amt = 0
            total_purchase = 0
            total_return = 0
            total_paid = 0
            for pos_ord in pos_order:
                due_amt += pos_ord.amount_due
                total_purchase += pos_ord.amount_total
                total_paid += pos_ord.amount_paid
                if pos_ord.amount_total < 0:
                    total_return += abs(pos_ord.amount_total)

            if due_amt > 0:
                credit_limit = cus.employess_id.credit_limit
                credit_consumed = round(due_amt, 2)
                credit_remaining = round(credit_limit - credit_consumed, 2)
                phone = cus.employess_id.work_phone
                department = cus.employess_id.department_id.name
                employee_contruct_id = cus.employess_id.barcode
                total_credit_purchase += total_purchase
                total_credit_return += total_return
                total_credit_limit = total_credit_limit + credit_limit
                total_credit_consumed = total_credit_consumed + credit_consumed
                total_credit_remaining = total_credit_remaining + credit_remaining
                total_paid_amount += total_paid

                data.append({
                    'SL': i,
                    'contact_id': employee_contruct_id,
                    'name': cus['name'],
                    'phone': phone,
                    'department': department,
                    'total_purchase': total_purchase + total_return,
                    'total_paid': total_paid,
                    'total_return': total_return,
                    'net_purchase': credit_consumed,
                    'credit_remaining': credit_remaining,
                    'credit_limit': credit_limit,
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
            'total_remaining': round(total_credit_remaining, 2),
            'total_purchase': round(total_credit_purchase, 2),
            'total_return': round(total_credit_return, 2),
            'total_paid': round(total_paid_amount, 2),
        }

    def generate_xlsx_report(self, workbook, data, objects):
        data = dict(data or {})
        customers = self.env['res.partner'].browse(data['customer_ids'])
        configs = self.env['pos.config'].search([])
        data.update(self.get_credit_details(data['date_start'], data['date_stop'], customers.ids, configs))
        company = self.env.company.name
        # print data to Excel Sheet
        sheet = workbook.add_worksheet("Credit sales report")
        format1 = workbook.add_format({'font_size': 14, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 9, 'align': 'vcenter', })
        format3 = workbook.add_format({'font_size': 11, 'align': 'vcenter', 'bold': True})
        title = workbook.add_format({'font_size': 16, 'align': 'center', 'bold': True})

        sheet.merge_range(0, 2, 0, 5, company, title)

        sheet.merge_range(3, 0, 3, 1, "Business Unit", format1)
        sheet.merge_range(3, 2, 3, 3, data['branch_name'], format3)

        sheet.merge_range(4, 0, 4, 1, "Printing Date", format1)
        sheet.merge_range(4, 2, 4, 3, str(data['current_date']), format3)

        sheet.write(5, 0, "from", format3)
        sheet.write(5, 1, str(data['date_start']), format3)
        sheet.write(5, 2, "to", format3)
        sheet.write(5, 3, str(data['date_end']), format3)

        sheet.write(7, 0, "SL", format3)
        sheet.write(7, 1, "Contact ID", format3)
        sheet.write(7, 2, "Name", format3)
        sheet.write(7, 3, "Phone", format3)
        sheet.write(7, 4, "Department", format3)
        sheet.write(7, 5, "Total Purchase", format3)
        sheet.write(7, 6, "Total Paid", format3)
        sheet.write(7, 7, "Total Return", format3)
        sheet.write(7, 8, "Net Purchase", format3)
        sheet.write(7, 9, "Remaining", format3)
        sheet.write(7, 10, "Limit", format3)

        row = 8
        name_length = 0
        phone_number_length = 0
        for table_data in data['data']:
            col = 0
            sheet.write(row, col, table_data['SL'], format2)
            col += 1
            sheet.write(row, col, table_data['contact_id'], format2)
            col += 1
            sheet.write(row, col, table_data['name'], format2)
            col += 1
            sheet.write(row, col, table_data['phone'], format2)
            col += 1
            sheet.write(row, col, table_data['department'], format2)
            col += 1
            sheet.write(row, col, table_data['total_purchase'], format2)
            col += 1
            sheet.write(row, col, table_data['total_paid'], format2)
            col += 1
            sheet.write(row, col, table_data['total_return'], format2)
            col += 1
            sheet.write(row, col, table_data['net_purchase'], format2)
            col += 1
            sheet.write(row, col, table_data['credit_remaining'], format2)
            col += 1
            sheet.write(row, col, table_data['credit_limit'], format2)
            col += 1

            row += 1
            if table_data['name']:
                if name_length < len(table_data['name']):
                    name_length = len(table_data['name'])

            if table_data['phone']:
                if phone_number_length < len(table_data['phone']):
                    phone_number_length = len(table_data['phone'])

        sheet.write(row, 4, 'Total', format3)
        sheet.write(row, 5, data['total_purchase'], format3)
        sheet.write(row, 6, data['total_paid'], format3)
        sheet.write(row, 7, data['total_return'], format3)
        sheet.write(row, 8, data['total_credit'], format3)
        sheet.write(row, 9, data['total_remaining'], format3)
        sheet.write(row, 10, data['total_limit'], format3)

        if name_length > 0:
            sheet.set_column('C:C', name_length)
        if phone_number_length > 0:
            sheet.set_column('D:D', phone_number_length)

