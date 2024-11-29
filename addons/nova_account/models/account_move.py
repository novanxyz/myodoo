from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from math import floor


class AccountMove(models.Model):
  _inherit="account.move"

  attachment_ids = fields.One2many('ir.attachment', compute='_get_attachment_ids', string="Attachments")

  def _get_attachment_ids(self):
    attachments = self.env['ir.attachment'].search([
        '&',('res_model', '=', 'account.move'), ('res_id', 'in', self.ids),
        ]) 
    result = dict.fromkeys(self.ids, self.env['ir.attachment'])
    for attachment in attachments:
        result[attachment.res_id] |= attachment

    self.attachment_ids = result