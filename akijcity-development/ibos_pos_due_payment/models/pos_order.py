# -*- coding: utf-8 -*-
from odoo import models, fields, api
import json
from odoo.tools import date_utils

class due_payment(models.Model):
    _inherit = 'pos.order'

    @api.model
    def get_lines_new(self, ref, method):
        result = []
        order_id = self.search([('pos_reference', '=', ref)], limit=1)

        if order_id:
            new_vals = {
                'product_id': order_id.id,
                'total_amount': order_id.amount_total,
                'total_paid': order_id.amount_paid,
                'due': order_id.amount_due,
                'payment_method': method,
            }
        result.append(new_vals)
        return [result]

    @api.model
    def refresh_Order_List(self, orderlistid):
        orders = self.env['pos.order'].search([('id', '>', '0')])
        new_list = []
        if(orderlistid):
            for j in orders:
                raw_data = j.read()
                if raw_data[0]['id'] != orderlistid[0]:
                    new_list.append(raw_data[0])
                else:
                    break
        else:
            for j in orders:
                raw_data = j.read()
                new_list.append(raw_data[0])


        if(new_list):
            json_data = json.dumps(new_list, default=date_utils.json_default)
            return json_data
        else:
            return False


    @api.model
    def create_recorde(self, val_list):
        method = val_list['payment_method']

        order = self.env['pos.order'].search([('id', '=', val_list['order_id'])])
        if (order.id):
            payment_method = self.env['pos.payment.method'].search([('id', '=', method[0]['id'])])
            payment = {"amount": val_list['payment'], "payment_method_id": payment_method.id, "pos_order_id": order.id}
            payment_id = self.env["pos.payment"].sudo().create(payment)


        if (payment_id and val_list['due_amount'] > 0):
            order.write({'amount_total': val_list['total_amount'],
                         'amount_paid': val_list['total_paid'],
                         'amount_due': val_list['due_amount']})
        elif (payment_id and val_list['due_amount'] == 0):
            order.write({'amount_total': val_list['total_amount'],
                         'amount_paid': val_list['total_paid'],
                         'amount_due': val_list['due_amount'],
                         'state': 'paid'})


        raw_data = order.read()
        json_data = json.dumps(raw_data, default=date_utils.json_default)

        return json_data
