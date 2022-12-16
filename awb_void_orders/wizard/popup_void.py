# -*- coding: utf-8 -*-
"""imports from odoo lib"""
from odoo import api, fields, models,_  # @UnusedImport
from odoo.exceptions import UserError



"""Created a class and model for wizard action"""
class VoidPopup(models.TransientModel):
    _name =  'void.popup'
    _description = 'check pwd popup'
    
    awb_pwd = fields.Char(string = 'PASSWORD', copy=False, readonly=False, translate=False)
    awb_void_reason = fields.Char(string = 'Reason',copy=False, readonly=False, translate=False)
    
    def CheckPwd(self):
        """check the password and void the orders"""
        user = self.env.user
        po_id = self._context.get('active_id')
        model = self._context.get('active_model')
        if (user.pos_security_pin == self.awb_pwd):
            if (model == 'pos.order'):
                if po_id:
                    #pos_orders = self.env['pos.order']
                    pos_ordersd = self.env['pos.order'].search([('id', '=', int(po_id))])
                    related_invoice_id = self.env['account.move'].search(
                        [('pos_order_id', '=', pos_ordersd.id), ('move_type', '=', 'out_invoice')], limit=1)
                    ref = '%'+ related_invoice_id.name
                    related_journal_record = self.env['account.move'].search(
                    [('move_type', '=', 'entry'), ('ref', 'like', ref)], limit=1)
                    move_reversal = self.env['account.move.reversal'].with_context(active_model="account.move", active_ids=related_journal_record.id).create({
                        'date': related_journal_record.date,
                        'reason': self.awb_void_reason,
                        'refund_method': 'cancel',
                        'journal_id': related_journal_record.journal_id.id,
                        'move_ids': [(4, related_journal_record.id, 0)]
                    })
                    move_reversal.reverse_moves()
                    pos_ordersd.refund()
                    pos_ordersd.state = 'voided'
                    related_invoice_id.state = 'voided'
                    related_journal_record.state = 'voided'

                    #===========================================================
                    # pos_orders.voidOrders(po_id)
                    # 
                    # account_bank_statement_line = self.env['account.bank.statement.line'].search(
                    #     [('statement_id', 'in', pos_ordersd.session_id.statement_ids.ids)]
                    # )
                    # for line in account_bank_statement_line:
                    #     pos_order_id = line.pos_statement_id.id
                    #     pos_order = self.env['pos.order'].search(
                    #         [('id', '=', pos_order_id)]
                    #     )
                    #     if pos_order.invoice_cancel:
                    #         payment_acc_move_line = self.env['account.move.line'].search(
                    #             [('statement_line_id', '=', line.id)], limit=1)
                    #         account_payment = payment_acc_move_line.payment_id
                    #         account_payment.cancel_payment()
                    #===========================================================
                
        else:
            raise UserError(_("Wrong Password."))
        
    