from _datetime import datetime
from odoo import api, models, _
from odoo.exceptions import UserError


class ReportStockProductScrap(models.AbstractModel):
    _name = 'report.ibos_scrap_product_report.report_stock_product_scrap'
    _description = 'Stock Product Scrap Report'

    def get_lines(self, data=None):
        date_from = data['date_from']
        date_to = data['date_to']
        location_ids = data['location_ids']
        sortby = data['sortby']
        print("sort_date:", sortby)

        product_scrap_line = self.env['stock.move.line'].search([('date', '>=', date_from), ('date', '<=', date_to), ('picking_id', '=', False), ('location_id', 'in', location_ids)], order="" + sortby + " desc")
        print("product_scrap_line:", product_scrap_line)

        return product_scrap_line

    @api.model
    def _get_report_values(self, docids, data=None):
        print("data['form']:", data['form'])
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        return {
            'data': data['form'],
            'lines': self.get_lines(data.get('form')),
        }