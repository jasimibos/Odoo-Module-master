from odoo import api, fields, models, tools, _
from datetime import datetime
import pytz
from odoo.osv.expression import AND
import datetime
from datetime import timedelta, date

class purchase_report(models.AbstractModel):
    _name = "report.ibos_purchase_management.purchase_report_return_details"

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, vendor=False, session_ids=False):
        date_start_format = fields.Datetime.from_string(date_start).date()
        date_end_format = fields.Datetime.from_string(date_stop).date()
        domain = [('state', 'in', ['draft', 'sent', 'to approve', 'purchase', 'done', 'cancel'])]

        if date_start:
            date_start = fields.Datetime.from_string(date_start).replace(hour=00, minute=00, second=00)
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

        if vendor:
            domain = AND([domain, [('partner_id', 'in', vendor)]])

        domain = AND([domain,
                      [('date_order', '>=', fields.Datetime.to_string(date_start)),
                       ('date_order', '<=', fields.Datetime.to_string(date_stop))]
                      ])

        pruchase_order_list = self.env['purchase.order'].search(domain)
        stock_picking = self.env['stock.picking'].search(['&', ('origin', 'like', '%Return%'),('id', '=', pruchase_order_list.picking_ids.ids)])

        Transfer_id = ''
        vendor_name = ''
        amount_total = ''
        return_product_name = ''
        UOM = ''
        return_Quantity = 0.0
        date = ''
        lots_number = ''
        unit_price = 0.0
        unit_price_total = 0.0
        qty_total = 0.0
        total_total = 0.0
        current_date = datetime.date.today()
        data = []
        business_unit = ''

        for stc_pick in stock_picking:
            Transfer_id = stc_pick.name
            vendor_name = stc_pick.partner_id.name.split('(')[0]
            date = stc_pick.scheduled_date
            # product_id = stc_pick.product_id.id
            purchase_id = stc_pick.purchase_id.id
            business_unit = stc_pick.branch_id.name
            for p in stc_pick.move_line_ids_without_package:
                product_line = self.env['purchase.order.line'].search(['&', ('order_id', '=', purchase_id), ('product_id', '=', p.product_id.id)])
                unit_price = product_line.price_unit
                return_product_name = p.product_id.partner_ref
                UOM = p.product_uom_id.name
                return_Quantity = p.qty_done
                lots_number = p.lot_id.name
                amount_total = round(unit_price * return_Quantity, 2)
                data.append({'Transfer_id':Transfer_id,
                            'vendor_name':vendor_name,
                            'return_product_name':return_product_name,
                            'UOM':UOM,
                            'return_Quantity':return_Quantity,
                            'date': date.date(),
                            'lot_number': lots_number,
                            'amount_total': amount_total,
                            'unit_price': unit_price})
            unit_price_total += unit_price
            qty_total += return_Quantity
            total_total += amount_total
        # End of for loop
        return {
            'date_start': date_start_format,
            'date_end': date_end_format,
            'current_date': current_date,
            'all_return_data': data,
            'unit_price_total': round(unit_price_total, 2),
            'qty_total': round(qty_total, 2),
            'total_total': round(total_total, 2),
            'business_unit': business_unit
        }

    def _get_report_values(self, docids, data=None):
        data = dict(data or {})
        vendors = self.env['res.partner'].browse(data['vendor_ids'])
        data.update(self.get_sale_details(data['date_start'], data['date_stop'],vendors.ids))
        return data


