import time

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class StockScrap(models.TransientModel):
    _name = 'stock.scrap.product.wizard'

    date_from = fields.Date(default=lambda *a: time.strftime('%Y-%m-%d'))
    date_to = fields.Date(default=lambda  *a: time.strftime('%Y-%m-%d'))
    location_ids = fields.Many2many('stock.location', string='Location', domain=[('usage', '=', 'internal')])
    sortby = fields.Selection([('date', 'Date'), ('location_id', 'Location')], default='date', string='Sort By')

    @api.model
    def default_get(self, fields):
        res = super(StockScrap, self).default_get(fields)
        location_id = False

        location_id = self.env['stock.location'].search([('usage', '=', 'internal')])
        print("location_id:", location_id)
        res.update({
            'location_ids': location_id.ids
        })
        return res
    def _build_contexts(self, data):
        result = {}
        result['location_ids'] = 'location_ids' in data['form'] and data['form'][
            'location_ids'] or False
        result['date_from'] = data['form']['date_from'] or False
        result['date_to'] = data['form']['date_to'] or False
        return result

    def print_scrap_product_report(self):
        self.ensure_one()
        if not self.date_from and not self.date_to:
            raise UserError(_("You must choose a start and end date"))
        if not self.location_ids:
            raise UserError(_("You must choose location"))

        data = {}
        data['ids'] = self.env.context.get('active_ids', [])
        data['model'] = self.env.context.get('active_model', 'ir.ui.menu')
        print("data data:", data)
        data['form'] = self.read(
            ['date_from', 'date_to', 'location_ids', 'sortby'])[0]

        used_context = self._build_contexts(data)
        data['form']['used_context'] = dict(used_context,
                                            lang=self.env.context.get(
                                                'lang') or 'en_US')
        print("data:", data)
        return self.env.ref('ibos_scrap_product_report.action_report_scrap_product').report_action(self, data=data)
