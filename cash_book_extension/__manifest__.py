# -*- coding: utf-8 -*-
{
    'name': "cash_book_extension",

    'summary': """
        Changes in Expenses Form""",

    'description': """
        Changes in Expenses Form
    """,

    'author': "Enterprise Cube (Pvt) Limited",
    'website': "http://ecube.pk",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','account'],

    # always loaded
    'data': [
        'views/views.xml',
    ],
}
