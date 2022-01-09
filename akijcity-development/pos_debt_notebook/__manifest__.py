{
    "name": "POS: Prepaid credits",
    "summary": "Comfortable sales for your regular customers. Debt payment method for POS",
    "category": "Point Of Sale",
    "images": ["images/debt_notebook.png"],
    "version": "13.0.5.3.5",
    "author": "IT-Projects LLC, Ivan Yelizariev",
    "support": "apps@itpp.dev",
    "website": "https://github.com/itpp-labs/pos-addons",
    "license": "Other OSI approved licence",  # MIT
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["point_of_sale"],
    "data": [
        "security/pos_debt_notebook_security.xml",
        "data/product.xml",
        "data/data.xml",
        "views/pos_debt_report_view.xml",
        "views/views.xml",
        "views/pos_credit_update.xml",
        "wizard/pos_credit_invoices_views.xml",
        "wizard/pos_credit_company_invoices_views.xml",
        "security/ir.model.access.csv",
        "views/res_partner.xml",
    ],
    "qweb": ["static/src/xml/pos.xml"],
    "demo": ["data/demo.xml"],
    "installable": True,
    "uninstall_hook": "pre_uninstall",
    "demo_title": "POS Debt/Credit Notebook",
    "demo_addons": [],
    "demo_addons_hidden": [],
    "demo_url": "pos-debt-notebook",
    "demo_summary": "Comfortable sales for your regular customers.",
    "demo_images": ["images/debt_notebook.png"],
}
