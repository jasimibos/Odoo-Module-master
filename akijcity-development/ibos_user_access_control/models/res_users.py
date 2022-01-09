from odoo import fields, models, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    def action_clear_access_control(self):
        user_id = self.id
        res_groups = self.env['res.groups'].search([('users', 'in', user_id)])
        for group in res_groups:
            if group.name != 'Internal User':
                group.write({'users': [(3, user_id)]})