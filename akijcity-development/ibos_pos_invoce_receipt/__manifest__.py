# -*- coding: utf-8 -*-
# Part of Nuro Solution Pvt Ltd.
{
    'name': 'POS Invoice Receipt via iBOS',
    'version': '13.0.1.0.3',
    'summary': """Pos Custom Receipt change previous pos receipt, added barcode in bottom""",
    'sequence': -20,
    'description': """
                    Change Odoo POS Receipt
                    Odoo POS Receipt new format
                    New Odoo POS Receipt                                      
                    """,
    'author': "ibos limited",
    'category': 'Sales/Point Of Sale',
    'website': 'ibos@ibos.io',
    'support': 'skmridul090@gmail.ocm',
    'company': 'iBOS Limited',
    'license': 'OPL-1',
    'images': [],
    'depends': ['base', 'point_of_sale'],
    "data": [
        'views/import.xml',
        'views/pos_order.xml',
    ],
    'demo': [],
    'qweb': ['static/src/xml/pos.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
