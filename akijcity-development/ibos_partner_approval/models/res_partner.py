from odoo import fields, models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([('draft', 'Draft'), ('submit', 'Submitted'), ('approved', 'Approved'), ('refused', 'Refused')], string='States', default='draft')


    def action_partner_approve(self):
        self.write({'state': 'approved'})

    def action_partner_submit_to(self):
        self.write({'state': 'submit'})

    def action_partner_refuse(self):
        self.write({'state': 'refused'})

    def action_partner_draft(self):
        self.write({'state': 'draft'})

