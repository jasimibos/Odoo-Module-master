from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang


class PurchaseOrderInherit(models.Model):
    _inherit = "purchase.order"

    purchase_order_approve_by = fields.Many2one('res.users', string='Approved By')

    def button_approve(self, force=False):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        self.write({'purchase_order_approve_by': user.id})
        # print("name",user.name,' id',user.id)
        return super(PurchaseOrderInherit, self).button_approve()



