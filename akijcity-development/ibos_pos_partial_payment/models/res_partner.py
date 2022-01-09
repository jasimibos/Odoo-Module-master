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
import json

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    total_due = fields.Monetary(compute='_total_due', string="Total Due")

    def _total_due(self):
        order = self.env['pos.order'].search([('partner_id', '=', self.id)])
        customer_credit_payment_list = self.env['customer.credit.payment.line'].search(
            [('partner_id', '=', self.id)])

        total_due = 0.0
        total = 0.0
        total_paid = 0.0
        credit_payment = 0.0

        for ord in order:
            total += ord["amount_total"]
            total_paid += ord["amount_paid"]

        for i in customer_credit_payment_list:
            credit_payment += i.amount

        total_due = (total - total_paid) - credit_payment

        if total_due:
            self.total_due = total_due
        else:
            self.total_due = 0.0

    def action_view_partner_dues(self):
        return {
            'name': _('Due order list'),
            'type': 'ir.actions.act_window',
            'res_model': 'pos.order',
            'view_id': False,
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.id), (('amount_due', '>', 0))],
        }

