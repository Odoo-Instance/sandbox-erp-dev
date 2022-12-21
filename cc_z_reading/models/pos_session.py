import base64

from datetime import datetime, timedelta
from odoo import _, api, fields, models
from odoo.osv.expression import AND


class PosSession(models.Model):
    _inherit = "pos.session"

    def generate_report(self, cc_z_reading_id):
        data = {
            'date_start': cc_z_reading_id.start_date,
            'date_stop': cc_z_reading_id.end_date,
            'company_name': cc_z_reading_id.env.company.name,
            'total_sales': cc_z_reading_id.total_sales,
            'total_returns': cc_z_reading_id.total_returns,
            'total_voids': cc_z_reading_id.total_voids,
            'total_discounts': cc_z_reading_id.total_discounts,
            'subtotal': cc_z_reading_id.subtotal,
            'vatable_sales': cc_z_reading_id.vatable_sales,
            'vat_12': cc_z_reading_id.vat_12,
            'vat_exempt_sales': cc_z_reading_id.vat_exempt_sales,
            'zero_rated_sales': cc_z_reading_id.zero_rated_sales,
            'register_total': cc_z_reading_id.register_total,
            'regular_discount': cc_z_reading_id.regular_discount,
            'beginning_reading': cc_z_reading_id.beginning_reading,
            'ending_reading': cc_z_reading_id.ending_reading,
        }
        print(cc_z_reading_id)
        data.update(cc_z_reading_id.get_payments(data['date_start'], data['date_stop']))
        print(data)
        return data

    def clossing_session_report(self):
        cc_z_reading_id = self.env['cc_z_reading.z_reading'].with_context(pos_close_report=True).create({
            'start_date': self.start_at,
            'end_date': fields.datetime.now() + timedelta(seconds=3),
            'crm_team_id': self.crm_team_id.id,
            'session_ids': [(6, 0, self.ids)],
        })
        data = self.generate_report(cc_z_reading_id)
        pdf = self.env.ref('cc_z_reading.action_z_reading_report').sudo()._render_qweb_pdf(cc_z_reading_id.id, data)[0]
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
        result = base64.b64encode(pdf)
        attachment_obj = self.env['ir.attachment']
        attachment_id = attachment_obj.sudo().create(
            {'name': "Z-reading", 'store_fname': 'name.pdf', 'datas': result})
        download_url = '/web/content/' + str(attachment_id.id) + '?download=true'
        print(attachment_id)
        # print(result)
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {"url": str(base_url) + str(download_url)}
