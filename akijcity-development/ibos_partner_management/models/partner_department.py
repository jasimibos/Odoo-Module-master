from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CustomerDepartment(models.Model):
    _name = "res.partner.department"
    _description = "Customer Department"
    _inherit = ['mail.thread']
    _order = "name"
    _rec_name = 'complete_name'

    name = fields.Char('Department Name', required=True)
    complete_name = fields.Char('Complete Name', compute='_compute_complete_name', store=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', index=True, default=lambda self: self.env.company)
    parent_id = fields.Many2one('res.partner.department', string='Parent Department', index=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    child_ids = fields.One2many('res.partner.department', 'parent_id', string='Child Departments')
    note = fields.Text('Note')
    color = fields.Integer('Color Index')

    def name_get(self):
        if not self.env.context.get('hierarchical_naming', True):
            return [(record.id, record.name) for record in self]
        return super(CustomerDepartment, self).name_get()

    @api.model
    def name_create(self, name):
        return self.create({'name': name}).name_get()[0]

    @api.depends('name', 'parent_id.complete_name')
    def _compute_complete_name(self):
        for department in self:
            if department.parent_id:
                department.complete_name = '%s / %s' % (department.parent_id.complete_name, department.name)
            else:
                department.complete_name = department.name

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive departments.'))

    def res_partner_action_customer(self):
        return {
            'name': _('Customer'),
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'domain': [('partner_department_id', '=', self.id)],
        }

