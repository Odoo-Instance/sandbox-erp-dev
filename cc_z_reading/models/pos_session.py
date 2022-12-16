import base64

from odoo import _, api, fields, models
from odoo.osv.expression import AND



class PosOrder(models.Model):
    _inherit = "pos.session"
    def clossing_session_report(self):
        pdf = self.env.ref('cc_z_reading.action_z_reading_report').sudo()._render_qweb_pdf(1)[0]
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        result = base64.b64encode(pdf)
        attachment_obj = self.env['ir.attachment']
        attachment_id = attachment_obj.sudo().create(
            {'name': "Z-reading", 'store_fname': 'name.pdf', 'datas': result})
        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
        print(attachment_id)
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {"url": str(base_url) + str(download_url)}
