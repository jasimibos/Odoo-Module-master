{
    "name": "User Access Control",
    "summary": """ User Access Control""",
    "category": "Tools",
    "images": [],
    "version": "13.0.1.0.0",
    "application": False,
    "author": "iBOS, Kamrul",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "branch", "stock", "purchase", "point_of_sale", "hr", "branch_customized"],
    "data": [
        "security/ir.model.access.csv",
        "security/menu_security.xml",
        "security/user_security.xml",
        'views/salesman_security_views.xml',
        'views/res_users.xml',
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
