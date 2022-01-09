from odoo import api, fields, models


class ReportTimesheet(models.AbstractModel):
    _name = 'report.timesheets_by_employee.report_timesheets'
    _description = 'Timesheet Report'

    def get_timesheets(self, docs):
        if docs.from_date and docs.to_date:
            record = self.env['account.analytic.line'].search(
                [('user_id', '=', docs.user_id[0].id),
                 ('date', '>=', docs.from_date), ('date', '<=', docs.to_date)])
