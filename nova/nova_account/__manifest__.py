# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Vardion Account',
    'version': '1.0',
    'author': 'Novan Firmansyah',
    'depends': ['web','vardion_brand','account'],
    'data': [
        'data/account.xml',
#        'data/resource.xml',
#        'data/barcodes.xml',
        'wizard/account_partner_reconcile.xml',
        'views/reports.xml',
        'views/views.xml',

    ],
    'qweb' : [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
    'description': """
    Additional Accounting features for all Vardion Projects
    
    """,
    'summary': 'Vardion Base Accounting Functionalities',
}
