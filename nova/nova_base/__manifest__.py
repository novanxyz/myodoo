# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Nova Base',
    'version': '1.0',
    'author': 'Novan Firmansyah',
    'depends': ['web','base','product','resource'],
    'website' : "https://novaarthama.com/",
    'category': "base",    
    'data': [
        'data/base.xml',
        'views/report.xml',
        'views/webclient_templates.xml',
    ],
    'qweb' : [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
    'description': """
    Additional base feature for all Nova Projects
    """,
    'summary': 'Nova Base Functionalities',
    'license' :  'AGPL-3',
}
