# -*- coding: utf-8 -*-
# Part of Nuro Solution Pvt Ltd.
{
    'name': 'Product Low Stock Alert',
    'version': '13.0.1.0.0',
    'summary': """Inventory product low stock alert """,
    'sequence': 10,
    'description': """
                    Inventory product low stock alert                                   
                    """,
    'author': "iBOS Limited, Kamrul Hasan",
    'category': 'Operations/Inventory',
    'website': 'https://ibos.io',
    'support': 'info@ibos.io',
    'company': 'iBOS Limited',
    'license': 'OPL-1',
    'images': [],
    'depends': ['base', 'stock', 'product'],
    "data": [
        'views/product_template.xml',
        'views/product_product.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
