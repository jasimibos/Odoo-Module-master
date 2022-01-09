from odoo import fields, models, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    bank_id = fields.Many2one('res.bank', string='Bank Name')
    bank_acc_no = fields.Many2one('res.partner.bank', string='Bank A/C', domain="[('bank_id', '=', bank_id), ('partner_id', '=', partner_id)]")
    bank_reference = fields.Char(copy=False)
    cheque_reference = fields.Char(copy=False)
    effective_date = fields.Date('Effective Date',
                                 help='Effective date of PDC', copy=False,
                                 default=False)

    def get_string_value_of_selection(self, value):
        return dict(self._fields['bank_name'].selection).get(self.bank_name)