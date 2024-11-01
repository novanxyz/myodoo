from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from math import floor

class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"
    _description = "Payment Term"
    _order = "name"
    
    def compute(self, value, date_ref=False): 
        self.ensure_one()       
        if self.env.context.get('currency_id'):
            currency = self.env['res.currency'].browse(self.env.context['currency_id'])
        else:
            currency = self.env.user.company_id.currency_id
        prec = currency.decimal_places
        amount = value
        result = []
        for line in self.line_ids:
            if line.value == 'fixed':
                amt = round(line.value_amount, prec)
            elif line.value == 'percent':
                amt = round(value * (line.value_amount / 100.0), prec)
            elif line.value == 'balance':
                amt = round(amount, prec)
            if amt:
                next_date = fields.Date.from_string(date_ref)
                if line.option == 'fixed_date':
                    m = int(floor(line.days/30))
                    next_date += relativedelta(months=m)                    
                    next_date = next_date.replace(day=line.fixed_date)
                    result.append((fields.Date.to_string(next_date), amt))
                    amount -= amt
        result += super(AccountPaymentTerm,self).compute(amount,date_ref)[0]                
        return result
    
class AccountPaymentTermLine(models.Model):
    _inherit = "account.payment.term.line"
    
    option      = fields.Selection(selection_add=[('fixed_date',_('Fixed Date after (days/30) month') )] )
    fixed_date  = fields.Integer("Fixed Date",default=1)
