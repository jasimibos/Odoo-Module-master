# -*- coding: utf-8 -*-
{
    'name': "iBOS POS Sales Report",

    'summary': """
        Sales report of Point of sale""",
    'sequence': -28,
    'description': """
        New Sales report for pos
    """,
    'author': "iBOS Limited",
    'website': "http://ibos.io",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sales_menu.xml',
        'wizard/pos_details.xml',
        'views/sales_details_new_report.xml',
        'views/pos_report_saledetails.xml',
        'views/assets.xml',
    ],
    'qweb': [],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
