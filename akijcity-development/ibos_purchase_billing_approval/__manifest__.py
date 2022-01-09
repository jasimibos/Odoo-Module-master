{
    "name": "Purchase Billing Approval",
    "summary": """ Purchase billing approval by manager/administrator """,
    "category": "Tools",
    "images": [],
    "version": "13.0.1.0.0",
    "application": False,
    "author": "iBOS, Kamrul",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "branch", "purchase",],
    "data": [
        'views/account_move.xml',
        'views/vendor_bill_action.xml',
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