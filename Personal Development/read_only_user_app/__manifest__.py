# -*- coding: utf-8 -*-

{
    'name': 'Read Only User Access',
    "author": "iBOS Limited",
    'version': '15.0.1.0',
    'summary': "Read only access to user limited access rights to user user limited access",
    'description': """  """,
    "license": "OPL-1",
    "images": ['static/description/screen_short.png'],
    'depends': ['base', 'sale_management'],
    'data': [
        'security/user_read_only_group.xml',
        'security/ir.model.access.csv',
        'views/res_user_read_only.xml',
    ],
    'installable': True,
    'auto_install': False,
    'category': 'Extra Tools',
}
