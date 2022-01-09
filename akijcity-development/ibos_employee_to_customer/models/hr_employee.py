# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import url_encode

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.exceptions import ValidationError, AccessError


class HrEmployeePrivate(models.Model):
    _inherit = "hr.employee"

    customer_id = fields.Many2one('res.partner', readonly=True, default=lambda self: self.customer_id.name) #compute='get_customer_name'
    credit_limit = fields.Float(string="Credit Limit", default=0.0, track_visibility='always', readonly=False)
    # customer_name = fields.Char(string="Customer", related='customer_id.name')

    @api.model
    def create(self, vals):
        if vals.get('user_id'):
            user = self.env['res.users'].browse(vals['user_id'])
            vals.update(self._sync_user(user))
            vals['name'] = vals.get('name', user.name)

        employee = super(HrEmployeePrivate, self).create(vals)

        cus_name = vals['name']
        if vals['barcode']:
            cus_name = cus_name + "(" + vals['barcode'] + ")"

        partner = self.env['res.partner'].sudo().create({
            'name': cus_name,
             "company_type": 'person',
             "image_1920": vals['image_1920'],
             'phone': vals['work_phone'],
             'mobile': vals['mobile_phone'],
             'email': vals['work_email'],
             'employess_id': employee.id,
             'customer_rank': 1,
             'supplier_rank': 1
        })

        employee.customer_id = partner.id
        return employee

    def write(self, vals):
        customer = self.env['res.partner'].search([('id', '=', self.customer_id.id)])
        if vals.get('name'):
            cus_name = vals['name']
            cus_name = cus_name + " (" + self.barcode + ")"

            customer.update({
                'name': cus_name
            })

        if vals.get('barcode'):
            cus_name = self.name
            cus_name = cus_name + " (" + vals.get('barcode') + ")"

            customer.update({
                'name': cus_name
            })

        if vals.get('mobile_phone'):
            customer.update({
                'mobile': vals.get('mobile_phone')
            })

        if vals.get('work_phone'):
            customer.update({
                'phone': vals.get('work_phone')
            })

        if vals.get('work_email'):
            customer.update({
                'email': vals.get('work_email')
            })
        
        return super(HrEmployeePrivate, self).write(vals)


    def _set_default_customer_credit_limit(self):
        employees = self.env['hr.employee'].search([])
        for emp in employees:
            customer = self.env['res.partner'].search([('id', '=', emp.customer_id.id)])
            customer.update({
                'credit_limit': emp.credit_limit
            })