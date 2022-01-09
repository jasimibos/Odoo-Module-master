from odoo import models, fields


class BoecConfig(models.Model):
    _name = 'boec.config'
    name = fields.Char('Name')
    deal_week_product_id = fields.Many2one('product.product', domain=[('is_published', '=', True)],
                                           string='Deal of the Week Product')
    date_end = fields.Datetime(string='Counter End Date')
    max_price = fields.Integer(string="Maximum Price", default=10000)


class ThemeBoec(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_boec_post_copy(self, mod):
        self.enable_view('ibos_theme.boec_header')


class ProductInherited(models.Model):
    _inherit = "product.template"
    hot_deals = fields.Boolean(string="Hot Sale")
