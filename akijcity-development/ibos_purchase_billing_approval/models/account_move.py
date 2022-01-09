from odoo import fields, models, api, _
from odoo.exceptions import AccessError, UserError, ValidationError

class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection([('draft', 'To Approve'), ('to_approve', 'To Approve'), ('posted', 'Approved'), ('refused', 'Refused'), ('cancel', 'Cancel')])

    def action_refused(self):
        self.update({
            'state': 'refused'
        })

    def action_approve_vendor_bill(self):
        if any(move.type not in ('in_invoice', 'out_invoice') for move in self):
            raise ValidationError(_("This action isn't available for this document."))

        for move in self:
            move.write({'state': 'posted'})

    def action_refuse_vendor_bill(self):
        if any(move.type not in ('in_invoice', 'out_invoice') for move in self):
            raise ValidationError(_("This action isn't available for this document."))

        for move in self:
            if move.state == 'posted':
                raise UserError(_("Approved bills can't refused"))
            move.write({'state': 'refused'})