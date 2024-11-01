# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Nova Account',
    'version': '1.0',
    'author': 'Novan Firmansyah',
    'depends': ['web','web_responsive','account'],
    'data': [
        'data/account.xml',
#        'data/resource.xml',
#        'data/barcodes.xml',
        # 'wizard/account_partner_reconcile.xml',
        'wizard/account_payment_register.xml',
        'views/reports.xml',
        'views/invoices.xml',
        'views/receipts.xml',
        'views/views.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'static/src/css/account.css'
        ],
    },
    'qweb' : [
        # 'static/src/xml/*.xml',
    ],
    'installable': True,
    'auto_install': False,
    'description': """
    Additional Accounting features for all Nova Projects
    
    """,
    'summary': 'Nova Base Accounting Functionalities',
    'license' :  'AGPL-3',
}
