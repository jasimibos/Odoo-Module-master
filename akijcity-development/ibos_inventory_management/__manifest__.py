{
    "name": "Inventory Management by iBOS",
    "summary": """ Inventory Management """,
    "category": "Operations/Inventory",
    "images": [],
    "version": "13.0.1.0.0",
    "application": False,
    "author": "iBOS Limited, Kamrul Hasan",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "stock", "stock_account","point_of_sale"],
    "data": [
        'views/product_product.xml',
        'views/product_template.xml',
        'views/inventory_config_setting_view.xml',
        'views/product_template_readonly.xml',
        'views/stock_valuation_layer.xml',
    ],
    "qweb": [
    ],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}