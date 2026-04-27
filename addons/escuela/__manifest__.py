# -*- coding: utf-8 -*-
{
    'name': "escuela",

    'summary': "Módulo de prueba para gestión escolar",

    'description': """
Módulo de prueba creado con odoo scaffold para aprender la estructura básica de un módulo Odoo.
    """,

    'author': "Rocío",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}