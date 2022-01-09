from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    plu_no = fields.Integer(string='PLU No', tracking=True)
    default_code = fields.Char(string='Item Code', tracking=True)
    is_product_type_readonly = fields.Boolean(dafault=False)
    # type = fields.Selection(selection_add=[('product', 'Storable Product')], tracking=True, default='product', readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(ProductTemplate,self).default_get(fields)
        check_is_product_type_readonly = self.env['ir.config_parameter'].sudo().get_param(
            'ibos_inventory_management.is_product_type_readonly')

        if len(res)>0:
            if check_is_product_type_readonly:
                res['is_product_type_readonly'] = check_is_product_type_readonly

        return res

    @api.model
    def create(self, vals):
        res = super(ProductTemplate, self).create(vals)
        if 'attribute_line_ids' not in vals and 'plu_no' in vals and 'default_code' in vals:
            product_product = self.env['product.product'].search([('product_tmpl_id', '=', res.id)])
            product_product.update({
                'plu_no': res.plu_no,
                'default_code': res.default_code
            })
        return res

    def write(self, vals):
        if 'attribute_line_ids' not in vals:
            product_product = self.env['product.product'].search([('product_tmpl_id', '=', self.id)])
            if 'plu_no' in vals:
                product_product.update({
                    'plu_no': vals.get('plu_no'),
                })

            if 'default_code' in vals:
                product_product.update({
                    'default_code': vals.get('default_code')
                })
        return super(ProductTemplate, self).write(vals)
