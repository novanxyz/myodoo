# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Nova Account',
    'version': '1.0',
    'author': 'Novan Firmansyah',
    'depends': ['web','web_responsive','account','nova_base','web_digital_sign'],
    'data': [
        # 'data/account.xml',
#        'data/resource.xml',
#        'data/barcodes.xml',
        # 'wizard/account_partner_reconcile.xml',
        'wizard/account_payment_register.xml',
        # 'views/reports.xml',
        # 'views/invoices.xml',
        # 'views/receipts.xml',
        'views/views.xml',
        'report/invoice_report.xml',
        'report/receipts_report.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'nova_account/static/src/css/account.scss'
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
