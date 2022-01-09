# -*- coding: utf-8 -*-
{
    'name': "Partner Approval",

    'summary': """
         Partner approval
         """,
    'sequence': -36,
    'description': """
        Partner approval
    """,
    'author': "iBOS Limited",
    'website': "https://ibos.io",
    'category': 'Tools',
    'version': '13.0.1.0.0',
    'depends': ['base', 'contacts', 'purchase', 'point_of_sale'],
    # always loaded
    'data': [
        'security/security.xml',
        'views/assets.xml',
        'views/res_partner_approval.xml',
        'views/purchase_order_approval.xml',
        'views/pos_config.xml',
    ],
    'qweb': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
