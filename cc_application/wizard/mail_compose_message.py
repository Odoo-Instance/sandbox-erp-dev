
from odoo import models, fields, api, _

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, fields):
        res = super(MailComposeMessage, self).default_get(fields)
        if self._context.get('default_subject'):
            res['subject'] = self._context.get('default_subject')
        return res
