# -*- coding: utf-8 -*-
{
    'name': "Partner Management",

    'summary': """
         Partner Management
         """,
    'sequence': -36,
    'description': """
        Partner approval
    """,
    'author': "iBOS Limited",
    'website': "https://ibos.io",
    'category': 'Tools',
    'version': '13.0.1.0.0',
    'depends': ['base', 'contacts', 'purchase',],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_bank.xml',
        'views/partner_department.xml',
        'views/res_partner.xml',
    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
