from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    quantity_validation = fields.Boolean(string="Demand quantity validation")
    sales_prise_and_margin = fields.Boolean(string="Show Sales prise and margin during purchase")

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('ibos_purchase_management.quantity_validation',
                                                  self.quantity_validation)
        self.env['ir.config_parameter'].set_param('ibos_purchase_management.sales_prise_and_margin',
                                                  self.sales_prise_and_margin)
        return res

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        qty_valid = self.env['ir.config_parameter'].sudo().get_param('ibos_purchase_management.quantity_validation')

        sale_prise_and_mergin = self.env['ir.config_parameter'].sudo().get_param('ibos_purchase_management.sales_prise_and_margin')
        if(qty_valid):
            res.update(
                quantity_validation = qty_valid
            )
        if (sale_prise_and_mergin):
            res.update(
                sales_prise_and_margin = sale_prise_and_mergin
            )
        return res