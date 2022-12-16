from odoo import http
from odoo.http import request
import json


class ClosePosPopup(http.controller):
    @http.route('/pos/session', type='http', auth="public")
    def __pos__(self, generate_report):
        # return http.Response()
        return self.env['closing_session'].ClosePosPopup(generate_report)
