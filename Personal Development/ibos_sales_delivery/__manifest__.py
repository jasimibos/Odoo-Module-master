# -*- coding: utf-8 -*-
{
    'name': "iBOS Sales Delivery",

    'summary': """iBOS Sales Delivery Module""",

    'description': """
        Long description of module's purpose
    """,

    'sequence': -15,
    'author': "Hussain Ahmed",
    'website': "https://ibos.io/",

    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/sales_delivery.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}
