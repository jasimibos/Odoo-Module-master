{
    "name": "Crate Employee and Customer",
    "summary": """Create customer during creating Employee""",
    'sequence': -30,
    "category": "HR Employees",
    "images": [],
    "version": "13.0.1.0.2",
    "application": False,
    "author": "iBOS, Mridul",
    "support": "info@ibos.io",
    "website": "https://ibos.io",
    "license": "Other OSI approved licence",  # MIT
    "depends": ["base", "hr"],
    "data": [
        "views/partner.xml",
        "views/employee_credit_payment.xml"
    ],
    "qweb": [],
    "auto_install": False,
    "installable": True,
    'application': True,
}
