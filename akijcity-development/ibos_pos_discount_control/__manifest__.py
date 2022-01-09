# -*- coding: utf-8 -*-
{
    'name': "Discount Control on POS",

    'summary': """
         Credit Sales report of Point of sale""",
    'sequence': -36,
    'description': """
        New Credit Sales report for pos
    """,
    'author': "iBOS Limited",
    'website': "http://ibos.io",
    'category': 'Uncategorized',
    'version': '13.0.1.0.0',
    'depends': ['base', 'point_of_sale', 'odoo_report_xlsx'],
    # always loaded
    'data': [
        'views/assets.xml',
        'views/pos_config.xml',
    ],
    'qweb': [],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
