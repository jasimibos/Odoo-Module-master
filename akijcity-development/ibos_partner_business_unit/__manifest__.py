# -*- coding: utf-8 -*-
{
    'name': "Partner Business Unit Management",

    'summary': """
         Partner Business Unit Management
         """,
    'sequence': -36,
    'description': """
        Partner Business Unit Management
    """,
    'author': "iBOS Limited",
    'website': "https://ibos.io",
    'category': 'Tools',
    'version': '13.0.1.0.0',
    'depends': ['base', 'contacts'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/res_partner_business_unit.xml',
    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
