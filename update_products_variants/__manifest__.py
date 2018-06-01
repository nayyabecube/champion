# -*- coding: utf-8 -*-
{
    'name': "update_products_variants",

    'summary': """
        Module for update variants of products""",

    'description': """
        Module for update variants of products
    """,

    'author': "EhtishamFaisal",
    'website': "http://www.oxenlab.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}