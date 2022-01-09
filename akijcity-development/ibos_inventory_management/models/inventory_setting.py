from odoo import api, fields, models, _


class inventorycategory(models.TransientModel):
   _inherit = 'res.config.settings'

   group_product_category = fields.Boolean(string="Product Category to POS Category", implied_group='purchase.group_warning_purchase')
   mrp_inventory_and_purchase = fields.Boolean(string="Show MRP in Purchase and Inventory")
   is_product_type_readonly = fields.Boolean(string="Is Product type readonly")
   type = fields.Selection([('consu', 'Consumable'),
                            ('service', 'Service'),
                            ('product', 'Storable Product')], string='Product Type', default='consu')

   def set_values(self):
       res = super(inventorycategory, self).set_values()
       # print("quantity_validation is", self.quantity_validation, 'from set')
       self.env['ir.config_parameter'].set_param('ibos_inventory_management.group_product_category', self.group_product_category)
       self.env['ir.config_parameter'].set_param('ibos_inventory_management.mrp_inventory_and_purchase',
                                                 self.mrp_inventory_and_purchase)
       self.env['ir.config_parameter'].set_param('ibos_inventory_management.is_product_type_readonly',
                                                 self.is_product_type_readonly)
       self.env['ir.config_parameter'].set_param('ibos_inventory_management.type',
                                                 self.type)
       return res

   def get_values(self):
       res = super(inventorycategory, self).get_values()
       productcategory = self.env['ir.config_parameter'].sudo().get_param('ibos_inventory_management.group_product_category')
       show_mrp = self.env['ir.config_parameter'].sudo().get_param('ibos_inventory_management.mrp_inventory_and_purchase')
       is_product_readonly = self.env['ir.config_parameter'].sudo().get_param('ibos_inventory_management.is_product_type_readonly')
       type_check = self.env['ir.config_parameter'].sudo().get_param('ibos_inventory_management.type')
       if(productcategory):
           res.update(
               group_product_category = productcategory
           )
       if(show_mrp):
           res.update(
               mrp_inventory_and_purchase = show_mrp
           )
       if(is_product_readonly):
           res.update(
               is_product_type_readonly = is_product_readonly
           )
       if(type_check):
           res.update(
               type = type_check
           )
       return res