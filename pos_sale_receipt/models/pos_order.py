# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class PosOrder(models.Model):
    _inherit = "pos.order"

    increase_sequence = fields.Boolean(string='Increase Sequence', default=False)
    send_warning = fields.Boolean(string='Show Warning')
    remaining_sequence_number = fields.Integer(string='Remaning sequence', readonly=True, default=0)    

    @api.model
    def create_from_ui(self, orders, draft=False):
        res = super(PosOrder, self).create_from_ui(orders, draft)
        order_ids = [d['id'] for d in res if 'id' in d]
        return self.env['pos.order'].search_read(domain = [('id', 'in', order_ids)], fields = ['id', 'pos_reference', 'send_warning', 'remaining_sequence_number'])       

    @api.model
    def _complete_values_from_session(self, session, values):
        res = super(PosOrder, self)._complete_values_from_session(session, values)
        crm_team_record =  session.config_id.crm_team_id
        res['increase_sequence'] = True
        if crm_team_record.threshold_sequence_number < crm_team_record.current_sequence_number:
            res['send_warning'] = True
            res['remaining_sequence_number'] = crm_team_record.ending_sequence_number - crm_team_record.current_sequence_number
        if crm_team_record.ending_sequence_number <= crm_team_record.current_sequence_number:
            raise ValidationError(_('Receipt number reached threshold sequence number.'))
        if crm_team_record:
            if crm_team_record.sale_team_prefix_id and crm_team_record.ending_sequence_number > crm_team_record.current_sequence_number and res['increase_sequence']:
                res['increase_sequence'] = False        
                crm_team_record.current_sequence_number += 1
                current_sequence_number_with_format = str(crm_team_record.current_sequence_number).zfill(5)
                if crm_team_record.ending_sequence_number > pow(9,6):
                    length_of_ending_sequence_number = len(str(crm_team_record.ending_sequence_number))
                    current_sequence_number_with_format = str(crm_team_record.current_sequence_number).zfill(length_of_ending_sequence_number)
                res['pos_reference'] = crm_team_record.sale_team_prefix_id.name + ' ' + str(current_sequence_number_with_format)
        return res