from odoo import models, fields,_

class BarcodeNomenclature(models.Model):
     _inherit = 'barcode.nomenclature'
     
     user_id = fields.Many2one('res.users','Users')
     
     
class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type    = fields.Selection(selection_add=[
            ('res.users', _('Users'))
    ])
    action_id = fields.Many2one('ir.actions.actions','Action to Execute')