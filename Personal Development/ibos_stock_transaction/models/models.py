# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ibos_stock_transaction(models.Model):
#     _name = 'ibos_stock_transaction.ibos_stock_transaction'
#     _description = 'ibos_stock_transaction.ibos_stock_transaction'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
