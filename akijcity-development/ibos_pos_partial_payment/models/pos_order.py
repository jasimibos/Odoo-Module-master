import logging
import psycopg2
from odoo import api, fields, models, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class pos_order(models.Model):
    _inherit = "pos.order"

    amount_due = fields.Float(string='Total Due', default=0.0)
    state = fields.Selection(
        [('draft', 'New'), ('cancel', 'Cancelled'), ('paid', 'Paid'), ('done', 'Posted'), ('invoiced', 'Invoiced'),
         ('due', 'Due')],
        'Status', readonly=True, copy=False, default='draft')

    @api.model
    def create(self, values):
        session = self.env['pos.session'].browse(values['session_id'])
        values = self._complete_values_from_session(session, values)
        return super(pos_order, self).create(values)

    def write(self, vals):
        for order in self:
            if vals.get('state') and (vals['state'] == 'paid' or vals['state'] == 'due') and order.name == '/':
                vals['name'] = order.config_id.sequence_id._next()
        return super(pos_order, self).write(vals)

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(pos_order, self)._order_fields(ui_order)
        if ui_order['amount_due'] > 0:
            order_fields.update({
                'amount_due': ui_order['amount_due']
            })
        return order_fields

    @api.model
    def create_from_ui(self, orders, draft=False):
        order_ids = []
        for order in orders:
            existing_order = False
            if 'server_id' in order['data']:
                existing_order = self.env['pos.order'].search(
                    ['|', ('id', '=', order['data']['server_id']), ('pos_reference', '=', order['data']['name'])],
                    limit=1)
            if (existing_order and existing_order.state == 'draft') or not existing_order:
                order_ids.append(self._process_order(order, draft, existing_order))

        return self.env['pos.order'].search_read(domain=[('id', 'in', order_ids)], fields=['id', 'pos_reference'])

    @api.model
    def _process_order(self, order, draft, existing_order):
        """Create or update an pos.order from a given dictionary.

        :param pos_order: dictionary representing the order.
        :type pos_order: dict.
        :param draft: Indicate that the pos_order is not validated yet.
        :type draft: bool.
        :param existing_order: order to be updated or False.
        :type existing_order: pos.order.
        :returns number pos_order id
        """
        order = order['data']
        pos_session = self.env['pos.session'].browse(order['pos_session_id'])
        if pos_session.state == 'closing_control' or pos_session.state == 'closed':
            order['pos_session_id'] = self._get_valid_session(order).id

        pos_order = False
        if not existing_order:
            pos_order = self.create(self._order_fields(order))
        else:
            pos_order = existing_order
            pos_order.lines.unlink()
            order['user_id'] = pos_order.user_id.id
            pos_order.write(self._order_fields(order))

        self._process_payment_lines(order, pos_order, pos_session, draft)

        if not draft:
            try:
                pos_order.action_pos_order_paid()
            except psycopg2.DatabaseError:
                # do not hide transactional errors, the order(s) won't be saved!
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

        if pos_order.to_invoice and (pos_order.state == 'paid' or pos_order.state == 'due'):
            pos_order.action_pos_order_invoice()

        return pos_order.id

    def _process_payment_lines(self, pos_order, order, pos_session, draft):

        prec_acc = order.pricelist_id.currency_id.decimal_places

        order_bank_statement_lines= self.env['pos.payment'].search([('pos_order_id', '=', order.id)])
        order_bank_statement_lines.unlink()
        is_return_paid = False
        for payments in pos_order['statement_ids']:
            is_return_paid = True
            if not float_is_zero(payments[2]['amount'], precision_digits=prec_acc):
                order.add_payment(self._payment_fields(order, payments[2]))

        order.amount_paid = sum(order.payment_ids.mapped('amount'))

        if not draft and not float_is_zero(pos_order['amount_return'], prec_acc):
            cash_payment_method = pos_session.payment_method_ids.filtered('is_cash_count')[:1]
            if not cash_payment_method:
                raise UserError(_("No cash statement found for this session. Unable to record returned cash."))

            if pos_order['amount_return'] > 0 and pos_order['amount_total'] - pos_order['amount_paid'] <= 0:
                for payments in pos_order['statement_ids']:
                    if payments:
                        return_payment_vals = {
                            'name': _('return'),
                            'pos_order_id': order.id,
                            'amount': -pos_order['amount_return'],
                            'payment_date': fields.Datetime.now(),
                            'payment_method_id': cash_payment_method.id,
                        }
                        order.add_payment(return_payment_vals)
                if not is_return_paid:
                    order.amount_due = -pos_order['amount_return']
                else:
                    order.amount_due = 0
            else:
                return_payment_vals = {
                    'name': _('return'),
                    'pos_order_id': order.id,
                    'amount': -pos_order['amount_return'],
                    'payment_date': fields.Datetime.now(),
                    'payment_method_id': cash_payment_method.id,
                }
                order.add_payment(return_payment_vals)

    def _is_pos_order_paid(self):
        return float_is_zero(self._get_rounded_amount(self.amount_total) - self.amount_paid, precision_rounding=self.currency_id.rounding)

    def action_pos_order_paid(self):
        if not self._is_pos_order_paid():
            self.write({'state': 'due'})
            return self.create_picking()
        self.write({'state': 'paid'})
        return self.create_picking()