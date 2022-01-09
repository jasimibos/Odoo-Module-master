from odoo import api, fields, models, _, http
from odoo.exceptions import UserError


class InventoryReport(models.Model):
    _name = 'inventory.report.customize'
    _description = 'Timesheet Report Wizard'
    from_date = fields.Datetime(string="Starting Date")
    to_date = fields.Datetime(string="Ending Date")
    state = fields.Selection([('1', 'Transaction'), ('2', 'Movement')], string='Status')

    def get_report_values(self, data=None):
        data = {
            'model': 'inventory.report.customize',
            'form': self.read()[0]
        }

        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        state = data['form']['state']
        if state == "1":
            data_report = self.env.cr.execute(f"""SELECT sv.date as date,pt.name as pname, svl.quantity as qty, sw.name as warehouse, sl.name as location
                                                           FROM stock_valuation_layer as svl
                                                           LEFT JOIN product_template as pt ON pt.id = svl.product_id
                                                           LEFT JOIN stock_move as sv ON sv.id = svl.stock_move_id
                                                           LEFT JOIN stock_warehouse as sw ON sw.id = sv.warehouse_id
                                                           LEFT JOIN stock_location as sl ON sl.id = sv.location_id
                                                           LEFT JOIN stock_picking_type as sp ON sp.id = sv.picking_type_id
                                                           where sp.sequence_code!='INT' and (sv.date between '{from_date}' and  '{to_date}')""")
            result = self._cr.dictfetchall()
            print("Transaction")
        elif state == "2":
            data_report = self.env.cr.execute(f"""SELECT sv.date as date,pt.name as pname, svl.quantity as qty, sw.name as warehouse, sl.name as location
                    FROM stock_valuation_layer as svl
                    LEFT JOIN product_template as pt ON pt.id = svl.product_id
                    LEFT JOIN stock_move as sv ON sv.id = svl.stock_move_id
                    LEFT JOIN stock_warehouse as sw ON sw.id = sv.warehouse_id
                    LEFT JOIN stock_location as sl ON sl.id = sv.location_id
                    LEFT JOIN stock_picking_type as sp ON sp.id = sv.picking_type_id
                    where sp.sequence_code='INT' and (sv.date between '{from_date}' and  '{to_date}')""")
            result = self._cr.dictfetchall()

        def ref(xml_id):
            proxy = self.env['ir.model.data']
            return proxy._xmlid_lookup(xml_id)[2]

        tree_view_id = ref('inventory_report_customizer.view_inventory_product_customize_report')


        data = {
            'views': tree_view_id,
            'data': data,
            'result': result,
            'state': state,
            'context': dict(result),
        }

        print(data)

        return data
