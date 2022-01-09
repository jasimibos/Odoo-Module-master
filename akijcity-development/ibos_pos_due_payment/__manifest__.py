# -*- coding: utf-8 -*-
{
    'name': "iBOS POS Due Payment",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '13.0.1.0.4',
    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'ibos_pos_partial_payment', 'account'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/credit_deduction.xml',
        'views/credit_deduction_line.xml',
        'views/credit_payment_line.xml',
    ],
    'qweb': [
        'static/src/xml/views.xml',
        'static/src/xml/employee.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
