from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_department_id = fields.Many2one('res.partner.department', string='Department', tracking=True)
    barcode = fields.Char(string="Enroll/Contact ID", help="Use a barcode to identify this contact from the Point of Sale.", copy=False, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get("barcode"):
            vals['name'] = vals.get("name") + "(" + vals.get("barcode") + ")"
        print("self:", self.barcode, "vals:", vals.get("name"))

        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if self.barcode:
            if len(self.name.split('(')) > 1:
                name = self.name.split('(')[0]
            else:
                name = self.name
                vals['barcode'] = self.barcode

            vals['name'] = name + "(" + vals.get("barcode") + ")"
        return super(ResPartner, self).write(vals)