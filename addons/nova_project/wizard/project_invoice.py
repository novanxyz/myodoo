
from odoo import api, fields, models, _

class ProjectInvoice(models.TransientModel):
    _name = 'project.invoice'
    _description = "Generate Report Invoice"
 
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    stage_id = fields.Many2one('project.task.type', string="Stage")
    tag_id = fields.Many2one('project.tags', string="Tag")


    def action_generate_invoice(self):
        pass