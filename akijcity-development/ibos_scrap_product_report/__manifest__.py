{
    'name': 'Stock Scrap Products Report',
    'version': '13.0.0.0',
    'author': 'iBOS Limited',
    'summary': 'Stock Scrap Products Report',
    'description': """Stock Scrap Products Report""",
    'category': 'Stock',
    'website': 'https://ibos.io/',
    'license': 'AGPL-3',

    'depends': ['base', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/stock_scrap_product_view.xml',
        'report/stock_scrap_product_report_view.xml',
        'report/report.xml',
    ],

    'qweb': [],
    'images': [],

    'installable': True,
    'application': True,
    'auto_install': False,
}