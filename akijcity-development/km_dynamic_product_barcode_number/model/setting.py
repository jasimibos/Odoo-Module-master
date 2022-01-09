from odoo import fields, models, api


class ResConfigSettingExtend(models.TransientModel):
    _inherit = 'res.config.settings'

    barcode_prefix = fields.Char(size=2, default="99", required=True)

    def set_values(self):
        res = super(ResConfigSettingExtend, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('km_dynamic_product_barcode_number.barcode_prefix', self.barcode_prefix)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettingExtend, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(barcode_prefix=params.get_param('km_dynamic_product_barcode_number.barcode_prefix'))
        return res
