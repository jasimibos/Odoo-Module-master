{
    "name": "Employee Advance Payment Adjustment Ad by iBOS",
    "summary": """ Inventory Management """,
    "category": "HR Employees",
    "images": [],
    "version": "13.0.1.0.0",
    "application": False,
    "author": "iBOS Limited, Kamrul Hasan",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "stock", "account", "hr", "purchase"],
    "data": [
        'views/account_move.xml',
        'views/hr_employee_advance_payment.xml',
        'views/hr_employee.xml',
        'views/hr_employee_public.xml',
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