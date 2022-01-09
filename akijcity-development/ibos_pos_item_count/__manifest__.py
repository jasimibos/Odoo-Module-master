{
    "name": "POS Item Count",
    "summary": """ POS Item Count""",
    "category": "Tools",
    "images": [],
    "version": "13.0.1.0.0",
    "application": False,
    "author": "iBOS Limited, Kamrul Hasan",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "branch", "purchase",],
    "data": [
        'views/assets.xml',
    ],
    "qweb": [
        "static/src/xml/order_line.xml",
        "static/src/xml/pos.xml"
    ],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}