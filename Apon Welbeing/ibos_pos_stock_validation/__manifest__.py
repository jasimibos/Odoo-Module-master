{
    'name': 'Product stock alert',
    'version': '15.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Show stock alert when product quantity is less then or equal zero',
    'author': 'Mridul',
    'company': 'iBOS',
    'maintainer': 'iBOS',
    'images': [],
    'website': 'https://www.ibos.com',
    'depends': ['base', 'point_of_sale'],
    'data': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
        'point_of_sale.assets': [
            'ibos_pos_stock_validation/static/src/js/model.js',
        ],
        'web.assets_qweb': [
            'ibos_pos_stock_validation/static/src/xml/OrderlineNew.xml',
        ],
    },
}


