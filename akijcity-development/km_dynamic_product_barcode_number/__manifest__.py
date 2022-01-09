# -*- coding: utf-8 -*-
# Part of Kamrul Hasan. See LICENSE file for full copyright and licensing details.

{
    'name': "Generate Products Barcode",
    'summary':'This module using for odoo product barcode number generate. You can alos add prefix of your company.',
    'description': """ 
        Product and products variants barcode generate, You can set also your company barcode prefix
        odoo product barcode solution,
        product barcode number generate,
        product barcode number generator,
        barcode number generate odoo,
        odoo barcode number generate,
        product barcode,
        barcode generte,
        odoo barcode solution,
        automatic barcode generator,
        uniqe barcode generate,
        EAN13 barcode number generate,
        random barcode number generator odoo,
        odoo barcode fix,
    """,
    'version': '13.0.0.1',
    'category': 'Inventory',
    'author': 'Kamrul Hasan',
    'live_test_url': 'https://www.youtube.com/watch?v=Jfxbvd_2YfA',
    'price': '0',
    'website': 'http://kamrul.net',
    'sequence': 0,
    'depends': [
        'base',
        'stock',
    ],
    'demo': [],
    'data': [
        'wizards/product_product_barcode.xml',
        'wizards/product_template_barcode.xml',
        'views/setting.xml',
    ],
    'qweb': [],
    "currency": 'EUR',
    'installable': True,
    'application': True,
    'images': ['static/description/generate_product_barcode_banner.png'],
    'support': 'kamruldev66@gmail.com',
    "license": "OPL-1",
}
