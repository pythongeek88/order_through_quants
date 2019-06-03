# -*- coding: utf-8 -*-
{
    'name': "Order Through Quants",

    'summary': """You could make orders directly through quants""",

    'description': """
        New functionality it gives you:
            - bonus
            - bonus
            - bonus
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock'],

    # always loaded
    'data': [
        # 'security/security.xml',
        # 'security/ir.model.access.csv',
        'views/new.xml',

    ],


    'installable': True,
    'application': True,
}