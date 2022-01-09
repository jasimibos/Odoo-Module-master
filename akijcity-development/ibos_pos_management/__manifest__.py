{
    "name": "Point of sale Management",
    "summary": """Point of sale Management""",
    'sequence': -28,
    "category": "Point Of Sale",
    "images": [],
    "version": "13.0.1.0.3",
    "application": False,
    "author": "iBOS Mridul",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "point_of_sale", 'ibos_pos_invoce_receipt'],
    "data": [
        'view/pos_order_listview.xml',
        'view/resource.xml',
        'view/product_pricelist_view.xml',
        'view/update_pricelist.xml',
        'security/security.xml',
        'view/pos_config_view.xml',
        'view/pos_order_line_view.xml',
        'security/ir.model.access.csv'
    ],
    "qweb": ["static/src/xml/pos.xml"],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
    'application': True,
}

