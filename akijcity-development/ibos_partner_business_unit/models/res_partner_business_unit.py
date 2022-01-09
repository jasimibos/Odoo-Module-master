from  odoo import fields, models

class ResPartnerBusinessUnit(models.Model):
    _name = 'res.partner.business.unit'

    name = fields.Char(string="Nmae", required=True)
    company_id = fields.Many2one('res.company', string="Company", required=True)
    telephone = fields.Char(string='Telephone No')
    address = fields.Text('Address')