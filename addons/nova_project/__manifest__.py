# -*- coding: utf-8 -*-
{
    'name': 'Nova Project',
    "author": "Novan Firmansyah",
    'version': '14.0.1.0',
    "images":['static/description/main_screenshot.png'],
    'summary': "Print project and task report using different filter",
    'description': """This app helps user to print project and task report between start date and end date using different filter like user of project or task and task stage.
    Project task reports
    """,
    "license" : "OPL-1",
    'depends': ['nova_base','project'],
    'data': [
            # "security/ir.model.access.csv",
            "views/project_report_template.xml",
            "wizard/project_invoice.xml",
            "views/project_reports.xml",
            # "wizard/project_task_report_view.xml",
            # "wizard/project_task_report_template.xml",
            ],
    'installable': True,
    'auto_install': False,
    'category': 'Project',

}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
