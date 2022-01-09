{
    'name': 'Purchase Order Report',
    'version': '13.0.0.0',
    'author': 'iBOS Limited',
    'summary': 'Purchase Order report',
    'description': """Purchase order report""",
    'category': 'Purchase',
    'website': 'https://ibos.io/',
    'license': 'AGPL-3',

    'depends': ['base', 'purchase'],

    'data': [
        'report/purchase_order_templates_inherit.xml',
        'report/purchase_quotation_templates_inherit.xml',
        'report/report_invoice.xml',
    ],

    'qweb': [],
    'images': ['static/description/Banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}