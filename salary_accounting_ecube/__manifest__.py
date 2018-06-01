# -*- coding: utf-8 -*-
{
    'name': "salary_accounting_ecube",

    'summary': """
        Ecube""",

    'description': """
        salary_accounting_ecube
    """,

    'author': "Ecube",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'templates.xml',
    ],

}