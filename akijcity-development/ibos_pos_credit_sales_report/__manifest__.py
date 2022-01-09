# -*- coding: utf-8 -*-
{
    'name': "iBOS POS Credit Sales Report",

    'summary': """
         Credit Sales report of Point of sale""",
    'sequence': -36,
    'description': """
        New Credit Sales report for pos
    """,
    'author': "iBOS Limited",
    'website': "http://ibos.io",
    'category': 'Uncategorized',
    'version': '13.0.1.0.1',
    'depends': ['base', 'point_of_sale', 'odoo_report_xlsx'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/credit_report_menu.xml',
        'report/credit_sales_report.xml',
        'report/credit_report_template.xml',
        'wizard/credit_sales_report_details.xml',
        'views/credit_report_template.xml'
    ],
    'qweb': [],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
