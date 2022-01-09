{
    "name": "POS Stock",
    "summary": """POS stock Quantity in odoo """,
    "category": "Point Of Sale",
    "images": [],
    "version": "13.0.1.0.0",
    "application": False,
    "author": "iBOS, Kamrul",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "point_of_sale", "stock"],
    "data": [
        "views/pos_views.xml",
        "views/assets.xml"
    ],
    "qweb": [
        "static/src/xml/pos.xml"
    ],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}