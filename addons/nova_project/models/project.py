

from odoo import models, fields, _ 

class Project(models.Model):
    _inherit = 'project.project'
    
    attachment_ids = fields.Many2many('ir.attachment',compute='_compute_attachments')

    def _compute_attachments(self):
        attachment_ids = self.env['ir.attachment'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id)
        ])
        self.attachment_ids = attachment_ids.ids
        
class Task(models.Model):
    _inherit = 'project.task'
    
    attachment_ids = fields.Many2many('ir.attachment',compute='_compute_attachments')

    def _compute_attachments(self):
        attachment_ids = self.env['ir.attachment'].search([
            ('res_model', '=', self._name),
            ('res_id', '=', self.id)
        ])
        self.attachment_ids = attachment_ids.ids