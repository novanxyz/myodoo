from odoo import fields, models


class SSHTunnel(models.Model):
  _name = 'ssh.tunnel'
  _description = 'Model Signature'

  local_port=  fields.Integer("Local Port", default=8086)
  local_ip = fields.String("Local Interface to Attach")
  remote_port=  fields.Integer("Remote Port Port", default=8086)
  
  remote_host = fields.String("Remote SSH Host")
  remote_user = fields.String("Remote SSH User")
  ssh_key = fields.Binary('SSH Key')
  
  state = fields.String("State")
  last_connected= fields.DateTime("Last Connected Time")

  def connect(self):
    state = 'connected'
    

  def disconnect(self):
    state = 'disconnected'
    
    