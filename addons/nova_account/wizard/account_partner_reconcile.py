from odoo import api, fields, models, _

class PartnerReconcile(models.TransientModel):
    _name = 'account.partner.reconcile'
    _description = "Reconcile Partner AR/AP"
        
    def _get_invoices(self):        
        return self.env['account.invoice']
    
    # @api.multi
    def _get_name(self):
        for r  in self:
            r.name = 'Balance Reconcile of %s @ %s' % ( r.partner_id.name , str(r.date)) if r.partner_id else ""        

    name        = fields.Char("Name",compute=_get_name)
    partner_id  = fields.Many2one('res.partner',"Partner",default=lambda self:self._context.get('active_id',False), required=1 )
    journal_id  = fields.Many2one('account.journal',default=lambda self:self.env.ref('vardion_account.partner_reconcile_journal') , domain=[('type','=','general')], required=1)
    currency_id = fields.Many2one('res.currency',related='journal_id.currency_id')
    date        = fields.Date('Date',default=fields.Date.today(),required=1)
    start_date  = fields.Date("Start Date",default=fields.Date.from_string(fields.Date.today()).replace(day=1) )
    end_date    = fields.Date("End Date",default=fields.Date.today())
    
    ar_acc      = fields.Many2one('account.account',related='partner_id.property_account_receivable_id')
    ap_acc      = fields.Many2one('account.account',related='partner_id.property_account_payable_id')
    credit      = fields.Monetary(related='partner_id.credit')
    debit       = fields.Monetary(related='partner_id.debit')

    input_moves = fields.One2many('account.move.line',compute='_get_default_moves', readonly=1)
#    input_moves = fields.One2many('account.move.line',default=_get_default_moves,readonly=1)
    
    output_moves = fields.One2many('account.move.line',compute='_get_default_moves')
#    receivable_output = fields.One2many('account.move.line',default=_get_default_moves)
    move_output     = fields.Many2one('account.move')
    
    invoice_ids  = fields.One2many('account.invoice',compute='_get_default_moves',readonly=1)
    valid        = fields.Boolean(compute='_get_default_moves')
    
    
    @api.depends('partner_id')
    @api.onchange('partner_id','start_date','end_date','journal_id')
    def _get_default_moves(self):
        self.ensure_one()
                
        AccountMoveLine = self.env['account.move.line']
        domain = [('partner_id','=',self.partner_id.id)]        
        domain.append(('account_id','in', [self.ap_acc.id, self.ar_acc.id] ))
#        domain.append(('journal_id.type','in', ['sale', 'purchase'] ))        
        if self.start_date:
            domain.append(('date','>=',self.start_date))
        if self.end_date:
            domain.append(('date','<=',self.end_date))
        self.input_moves  = AccountMoveLine.search(domain)
        moves = self.input_moves.mapped('move_id')
        
        self.invoice_ids = self.env['account.invoice'].search([('move_id','in',moves.ids )])        
        
        self.output_moves = AccountMoveLine
        lines = self.get_reconcile_lines()
        for l in lines:        
            self.output_moves += AccountMoveLine.new(l)    
        self.valid = bool( sum(self.output_moves.mapped('credit')) )
    
    # @api.multi
    @api.depends('input_moves')
    def get_reconcile_lines(self):
        self.ensure_one()
        ar_acc = self.partner_id.property_account_receivable_id
        ap_acc = self.partner_id.property_account_payable_id
        
        tot_ap_deb = sum( self.input_moves.filtered(lambda l:l.account_id.id == ap_acc.id).mapped('debit'))
        tot_ap_cre = sum( self.input_moves.filtered(lambda l:l.account_id.id == ap_acc.id).mapped('credit'))
        
        tot_ap = tot_ap_cre - tot_ap_deb 
        
        
        tot_ar_deb = sum( self.input_moves.filtered(lambda l:l.account_id.id == ar_acc.id).mapped('debit'))
        tot_ar_cre = sum( self.input_moves.filtered(lambda l:l.account_id.id == ar_acc.id).mapped('credit'))
        
        tot_ar = tot_ar_deb  - tot_ar_cre 
        

        ar_move = {'account_id':ar_acc.id,'name': "AR Reconcile" ,'journal_id': self.journal_id.id,'partner_id' : self.partner_id.id }        
        ap_move = ar_move.copy()
        ap_move.update({'account_id':ap_acc.id,'name':'AP Reconcile'})

        ar_move.update({'credit':tot_ap ,'debit': 0  })                
        ap_move.update({'credit':0.0    ,'debit': tot_ap})
        
        if tot_ap > tot_ar:            
            ar_move.update({'credit':tot_ar ,'debit':      0  })
            ap_move.update({'credit':     0 ,'debit': tot_ar  })            
        return [ap_move,ar_move]
    
    
    # @api.multi
    def reconcile(self):    
        self.ensure_one()
        move = {'date': self.date,'name': self.name ,'journal_id': self.journal_id.id,}
        lines = self.get_reconcile_lines()      
        move['line_ids'] = map(lambda l: (0,0,l),lines)
        output = self.env['account.move'].create(move)
        output.post()
        self.move_output   = output.id
        return output
    
    # @api.multi
    def reconcile_invoice(self):
        self.ensure_one()
        move = self.reconcile()        
        invoices = self.invoice_ids.sorted(key=lambda i:i.date)
        inv_cnt = 0
        for aml in move.line_ids:            
#            print aml.read()            
            if aml.credit and aml.account_id.id == self.ar_acc.id :
                amount = aml.credit
                invs = invoices.filtered(lambda i: i.type == 'out_invoice' and i.state == 'open')                
                for inv in invs:                    
                    if amount >= inv.residual:
                        inv.assign_outstanding_credit(aml.id)
                        amount -= inv.residual
                
            
            if aml.debit and aml.account_id.id == self.ap_acc.id :
                amount = aml.debit
                invs = invoices.filtered(lambda i: i.type == 'in_invoice' and i.state == 'open')                
                for inv in invs:                    
                    if amount >= inv.residual:
                        inv.assign_outstanding_credit(aml.id)
                        amount -= inv.residual
        return {'warning': _('There is %d invoices reconciliated.\n Please re-check your Customer/Vendor Invoices') % inv_cnt }
        

