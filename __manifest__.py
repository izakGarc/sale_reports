# -*- coding: utf-8 -*-
{
    'name': "sale_reports",

    'summary': """
        Forza Report orders""",

    'description': """
        Forza Report orders
    """,

    'author': "Ili-Dev",
    'website': "https://www.yourcompany.com",

    'category': 'sale',
    'version': '19.0.1.0.0',

    'depends': ['sale'],

    'data': [
        'security/ir.model.access.csv',
        'report/report_sale.xml',
        'wizard/sale_report_wizard.xml',
    ],
}
