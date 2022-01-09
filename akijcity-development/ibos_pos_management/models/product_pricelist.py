from itertools import chain
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_repr
from odoo.tools.misc import get_lang

class Pricelist(models.Model):
    _inherit = "product.pricelist"

    def show_all_product_in_price_line(self):
        item_ids = [(5, 0, 0)]
        new_item = []
        product_rec = self.env['product.template'].search([])
        product_pricelist_rec = self.env['product.pricelist'].search([('id', '=', self.id)])
        existing_product_is_list = [rec for rec in product_pricelist_rec.item_ids.product_tmpl_id.ids]

        if len(product_pricelist_rec.item_ids) == 0:
            for pro in product_rec:
                line = (0, 0, {
                'product_tmpl_id': pro.id,
                'fixed_price': pro.list_price,
                'mrp': pro.mrp
                })
                item_ids.append(line)
            self.update({
                'item_ids': item_ids
            })
        if len(product_pricelist_rec.item_ids) > 0:
            for pro in product_rec:
                if pro.id not in existing_product_is_list:
                    line = (0, 0, {
                        'product_tmpl_id': pro.id,
                        'fixed_price': pro.list_price,
                        'mrp': pro.mrp
                    })
                    new_item.append(line)
            if len(new_item) > 0:
                self.update({
                    'item_ids': new_item
                })
        else:
            raise UserError(_("Already product add in the list"))
        return self

    # @api.onchange('item_ids')
    # def onchange_item_ids(self):
    #     print('current', self._origin.id, self.item_ids.product_tmpl_id.ids)
    #     product_pricelist_rec = self.env['product.pricelist'].search([('id', '=', self._origin.id)])
    #     print('previous', product_pricelist_rec.item_ids.product_tmpl_id.ids)

        # if len(product_pricelist_rec.item_ids.product_tmpl_id.ids) > 0:
        #     existing_product_list = [rec for rec in product_pricelist_rec.item_ids.product_tmpl_id.ids]
        #     print(existing_product_list)
        #     if self.item_ids.product_tmpl_id.ids in existing_product_list:
        #         raise UserError(_("Already product add in the list"))


