
{
    'name': 'Serial number in Sale Order,Purchase Order,Invoice',
    'version': '13.0.0.0',
    'author': 'iBOS Limited, Kamrul Hasan',
    'summary': 'Serial number in Sale Order Linee',
    'description': """This module helps to show serial number in sale order lines.""",
    'category': 'Base',
    'website': 'https://ibos.io/',
    'license': 'AGPL-3',

    'depends': ['sale_management', 'account', 'purchase'],

    'data': [
        'views/sale_order_views.xml',
        'report/sale_order_report.xml',
    ],

    'qweb': [],
    'images': ['static/description/Banner.png'],

    'installable': True,
    'application': True,
    'auto_install': False,
}
