from itertools import chain
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_repr
from odoo.tools.misc import get_lang

class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    mrp = fields.Float('MRP', readonly=False)
    can_modify_pricelist = fields.Boolean(string="Access for modify", default=False, compute="compute_pricelist_modify_access")

    @api.onchange('product_tmpl_id')
    def onchange_product_tmpl_id(self):
        product_template = self.env['product.template'].search([('id', '=', self.product_tmpl_id.id)])
        self.fixed_price = product_template.list_price
        self.fixed_price = product_template.list_price
        self.mrp = product_template.mrp
        # print(self.base_pricelist_id.id)
        # product_pricelist = self.env['product.pricelist'].search([('id', '=', self.base_pricelist_id.id)])
        # print('list', product_pricelist.item_ids.product_tmpl_id.ids)

    def compute_pricelist_modify_access(self):
        self.can_modify_pricelist = False
        if self.env.user.has_group('ibos_pos_management.group_price_list_approval'):
            self.can_modify_pricelist = True
        return True

    def write(self, vals):
        res = super(PricelistItem, self).write(vals)
        product_template = self.env['product.template'].search([('id', '=', self.product_tmpl_id.id)])
        product_template.write({
            'list_price': self.fixed_price,
            'mrp': self.mrp
        })
        return res