from odoo import fields, models, api

class ResBank(models.Model):
    _inherit = 'res.partner.bank'

    acc_branch_name = fields.Char(string='Branch Name')
    acc_branch_routing = fields.Char(string='Routing No')
    acc_branch_address = fields.Char(string='Branch address')
    acc_branch_checks_sheet = fields.Binary('Attachment', help="Upload your PDF file.")
