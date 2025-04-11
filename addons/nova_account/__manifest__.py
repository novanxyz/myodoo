# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Nova Account',
    'version': '1.0',
    'author': 'Novan Firmansyah',
    'depends': ['web','account','nova_base','web_digital_sign'],
    "website": "https://github.com/OCA/web",
    'data': [
        # 'data/account.xml',
#        'data/resource.xml',
#        'data/barcodes.xml',
        # 'wizard/account_partner_reconcile.xml',
        'report/invoice_report.xml',
        'report/receipts_report.xml',
        'wizard/account_payment_register.xml',
        'views/reports.xml',
        # 'views/invoices.xml',
        # 'views/receipts.xml',
        # 'views/views.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'nova_account/static/src/css/account.scss',
            'nova_account/static/src/js/account.js'
        ],
    },
    'qweb' : [
        # 'static/src/xml/*.xml',
    ],
    'category_id' : 'Accounting',
    'installable': True,
    'auto_install': False,
    'description': """
    Additional Accounting features for all Nova Projects
    
    """,
    'summary': 'Nova Base Accounting Functionalities',
    'license' :  'AGPL-3',
}
