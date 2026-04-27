# -*- coding: utf-8 -*-
{
    'name': "Marketing Digital",
    'summary': "Gestión de proyectos y servicios para agencia de marketing digital",
    'description': """
Módulo para la gestión integral de una agencia de marketing digital y diseño web.
Permite gestionar clientes, proyectos, tareas y servicios.
    """,
    'author': "Rocío",
    'website': "https://www.yourcompany.com",
    'category': 'Services',
    'version': '0.1',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/servicio_views.xml',
        'views/proyecto_views.xml',
        'views/tarea_views.xml',
        'views/menu_views.xml',
        'report/proyecto_report.xml',
        'report/proyecto_report_template.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}