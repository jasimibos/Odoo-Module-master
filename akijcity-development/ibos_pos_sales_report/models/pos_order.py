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

_logger = logging.getLogger(__name__)

class ReportSaleDetails(models.AbstractModel):
    _name = "report.ibos_pos_sales_report.pos_report_saledetails"
    _description = 'Point of Sale Details'


    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, configs=False, session_ids=False):

        date_start_format = fields.Datetime.from_string(date_start).date()
        date_end_format = fields.Datetime.from_string(date_stop).date()

        config_ids = configs.ids
        domain = [('state', 'in', ['paid','invoiced','done','due'])]
        if (session_ids):
            domain = AND([domain, [('session_id', 'in', session_ids)]])
        else:
            if date_start:
                date_start = fields.Datetime.from_string(date_start)
            else:
                # start by default today 00:00:00
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz or 'UTC')
                today = user_tz.localize(fields.Datetime.from_string(fields.Date.context_today(self)))
                date_start = today.astimezone(pytz.timezone('UTC'))
            if date_stop:
                date_stop = fields.Datetime.from_string(date_stop).replace(hour=23, minute=59, second=59)
                # avoid a date_stop smaller than date_start
                if (date_stop < date_start):
                    date_stop = date_start + timedelta(days=1, seconds=-1)
            else:
                # stop by default today 23:59:59
                date_stop = date_start + timedelta(days=1, seconds=-1)

            domain = AND([domain,
                [('date_order', '>=', fields.Datetime.to_string(date_start)),
                ('date_order', '<=', fields.Datetime.to_string(date_stop))]
            ])

            if config_ids:
                domain = AND([domain, [('config_id', 'in', config_ids)]])

        orders = self.env['pos.order'].search(domain)
        print("orders:", orders)

        user_currency = self.env.company.currency_id
        product_line = self.env['pos.order.line'].search(['&',('product_id','=',configs.discount_product_id.id),('order_id','=',orders.ids)])


        total = 0.0
        total_return = 0.0
        due = 0.0
        return_cradit = -0.0

        tz = pytz.timezone('Asia/Dhaka')
        current_date = datetime.now(tz=tz).strftime("%d-%m-%Y %I:%M %p")
        # cashier_name = orders.config_id.pos_session_username
        cash_earn = 0.0
        cash_return = 0.0
        credit_earn = 0.0
        credit_return = 0.0
        total_sales= 0.0
        total_discount = 0.0
        net_sale_total = 0.0

        order_ids = []
        order_return_ids = []
        pos_responsible_name = []
        sales = []
        return_ = [{'name':'Cash','total':0.0},{'name':'Credit','total':0.0}]

        methods = self.env['pos.payment.method'].search([])
        for m in methods:
            sales.append({'name':m.name,'total':0.0})

        sales.append({'name': 'Credit', 'total': 0.0})

        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        if user:
            pos_responsible_name.append({'name': user.name})

        for dis in product_line:
            total_discount = total_discount + abs(dis.price_subtotal)


        for order in orders:
            if user_currency != order.pricelist_id.currency_id:
                net_sale_total += order.pricelist_id.currency_id._convert(
                    order.amount_total, user_currency, order.company_id, order.date_order or fields.Date.today())
            else:
                net_sale_total += order.amount_total

            if order.amount_due > 0:
                due += order.amount_due
            if order.amount_due < 0.0:
                return_cradit = return_cradit + order.amount_due

            if len(order.lines) > 1:
                for ln in order.lines:
                    if ln.discount > 0.0:
                        total_discount = total_discount + ((ln.price_unit * ln.qty) - ln.price_subtotal )
            else:
                if order.lines.discount > 0.0:
                    total_discount = total_discount + ((order.lines.price_unit * order.lines.qty) - order.lines.price_subtotal )

            if order.amount_paid > 0.0:
                order_ids.append(order.id)
            if  order.amount_paid < 0.0 or order.amount_due < 0.0:
                order_return_ids.append(order.id)

            currency = order.session_id.currency_id

        ########################
        ### For Payment Query ###
        payment_ids = self.env["pos.payment"].search([('pos_order_id', 'in', order_ids)]).ids
        if payment_ids:
            self.env.cr.execute("""
                SELECT method.name, sum(amount) total
                FROM pos_payment AS payment,
                     pos_payment_method AS method
                WHERE payment.payment_method_id = method.id
                    AND payment.id IN %s
                GROUP BY method.name
            """, (tuple(payment_ids),))
            payments = self.env.cr.dictfetchall()
        else:
            payments = []


        payments.append({'name': 'Credit', 'total': due})

        for m in payments:
            total = total + m['total']
            if m['name'] == 'Cash':
                cash_earn = m['total']
            if m['name'] == 'Credit':
                credit_earn = m['total']
            for s in sales:
                if s['name'] == m['name']:
                    s['total'] = m['total']

        sales.append({'name': 'Total', 'total': total})

        ########################
        ### For Return Query ###
        payment_ids_for_return = self.env["pos.payment"].search([('pos_order_id', 'in', order_return_ids)]).ids
        if payment_ids_for_return:
            self.env.cr.execute("""
                SELECT method.name, sum(amount) total
                FROM pos_payment AS payment,
                     pos_payment_method AS method
                WHERE payment.payment_method_id = method.id
                    AND method.name = 'Cash'
                    AND payment.id IN %s
                GROUP BY method.name
            """, (tuple(payment_ids_for_return),))
            payments_return = self.env.cr.dictfetchall()
        else:
            payments_return = []

        payments_return.append({'name': 'Credit', 'total': return_cradit})

        for k in payments_return:
            total_return = total_return + k['total']
            k['total'] = abs(k['total'])
            if k['name'] == 'Cash':
                cash_return = k['total']
            if k['name'] == 'Credit':
                credit_return = k['total']
            for rt in return_:
                if rt['name'] == k['name']:
                    rt['total'] = k['total']

        return_.append({'name': 'Total', 'total': abs(total_return)})

        total_sales = total
        today_net_cash = cash_earn - cash_return
        today_net_credit = credit_earn - credit_return


        return {
            'currency_precision': user_currency.decimal_places,
            # 'todays_cash': user_currency.round(total),
            'total_due': due,
            'payments': sales,
            'print_date': current_date,
            'responsible_name': pos_responsible_name,
            'business_unit_name': configs.branch_id.name,
            'company_name': configs.branch_id.company_id.name,
            'company_address': configs.branch_id.company_id.street,
            'company_logo': configs.branch_id.company_id.logo,
            'returns_': return_,
            'net_cash': user_currency.round(today_net_cash),
            'net_credit': user_currency.round(today_net_credit),
            'total_invoice': len(orders),
            'total_sales': total_sales,
            'today_net_sales': user_currency.round(net_sale_total),
            'today_sale_return': abs(total_return),
            'today_discount': total_discount,
            'start_date': date_start_format.strftime("%d-%m-%Y"),
            'end_date': date_end_format.strftime("%d-%m-%Y")

        }

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        configs = self.env['pos.config'].browse(data['config_ids'])
        data.update(self.get_sale_details(data['date_start'], data['date_stop'], configs))
        return data