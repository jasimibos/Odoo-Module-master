# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PosCategory(models.Model):
    _inherit = 'pos.category'

    product_category_id = fields.Many2one('product.category', string='Product Category reference')