import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)

class ProductCategory(models.Model):
    _inherit = "product.category"

    product_category_ref = fields.Many2one('pos.category', string='Product category reference')

    property_cost_method = fields.Selection([
        ('standard', 'Standard Price'),
        ('fifo', 'First In First Out (FIFO)'),
        ('average', 'Average Cost (AVCO)')], string="Costing Method",
        company_dependent=True, copy=True, required=True,
        help="""Standard Price: The products are valued at their standard cost defined on the product.
                Average Cost (AVCO): The products are valued at weighted average cost.
                First In First Out (FIFO): The products are valued supposing those that enter the company first will also leave it first.
                """, default='average')

    property_valuation = fields.Selection([
        ('manual_periodic', 'Manual'),
        ('real_time', 'Automated')], string='Inventory Valuation',
        company_dependent=True, copy=True, required=True,
        help="""Manual: The accounting entries to value the inventory are not posted automatically.
                Automated: An accounting entry is automatically created to value the inventory when a product enters or leaves the company.
                """, default='real_time')

    @api.model
    def create(self, vals):
        res = super(ProductCategory, self).create(vals)
        product_category_check = self.env['ir.config_parameter'].sudo().get_param('ibos_inventory_management.group_product_category')
        if product_category_check:
            # print('name', res['name'], 'id', res['id'])
            pos_category = {'name': vals.get('name'), 'sequence': 0, 'product_category_id': res['id']}
            p_category = self.env["pos.category"].sudo().create(pos_category)
            res['product_category_ref'] = p_category.id
        return res


    def write(self, vals):
        pos_category = self.env['pos.category'].search([('id', '=', self.product_category_ref.id)])
        if vals.get('name') and pos_category:
                pos_category.update({
                    'name':vals.get('name')
                })
        return super(ProductCategory,self).write(vals)

    def unlink(self):
        self.env['pos.category'].search([('id', '=', self.product_category_ref.id)]).unlink()
        return super(ProductCategory, self).unlink()