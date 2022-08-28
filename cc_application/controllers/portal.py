# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

from odoo import http, _
from odoo.http import request, route
import json
from odoo.addons.portal.controllers.portal import CustomerPortal, \
    pager as portal_pager

from collections import OrderedDict
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
from odoo.osv.expression import AND

from odoo import SUPERUSER_ID


class PortalAccount(CustomerPortal):

    def _get_application_domain(self):
        return [('user_id', '=', request.env.user.id)]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'application_count' in counters:
            application_count = request.env['grant.application'].search_count(
                self._get_application_domain()) \
                if request.env['grant.application'].check_access_rights('read',
                                                                        raise_exception=False) else 0
            values['application_count'] = application_count
        return values

    @http.route(['/my/applications', '/my/applications/page/<int:page>'],
                type='http', auth="user", website=True)
    def portal_my_application(self, page=1, date_begin=None, date_end=None,
                              sortby=None, search=None, search_in='all',
                              groupby='none', filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        user_id = request.env.user
        Application_Id = request.env['grant.application'].sudo()
        default_domain = [('user_id', '=', user_id.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
        }

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': default_domain},
            'stage_id': {'label': _('Registration'), 'domain': AND(
                [default_domain, [('stage_id', '=', request.env.ref(
                    'cc_application.state_registration').id)]])},
        }

        searchbar_inputs = {
            'all': {'input': 'all', 'label': _('Search in All'), 'order': 1},
        }

        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None'), 'order': 1},
            'stage_id': {'input': 'stage_id', 'label': _('Stage')},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'
        sort_order = searchbar_sortings[sortby]['order']
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters[filterby]['domain']
        # search only the document name
        if search and search_in:
            domain = AND([domain, ['|', ('name', 'ilike', search), '|',
                                   ('business_name', 'ilike', search),
                                   ('project_name', 'ilike', search), ]])
        pager = portal_pager(
            url='/my/applications',
            url_args={'date_begin': date_begin, 'date_end': date_end,
                      'sortby': sortby, 'filterby': filterby,
                      'search_in': search_in, 'search': search},
            total=Application_Id.search_count(domain),
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        if groupby == 'stage_id':
            sort_order = 'stage_id, %s' % sort_order

        # search the count to display, according to the pager data
        applications = Application_Id.search(domain, order=sort_order,
                                             limit=self._items_per_page,
                                             offset=pager['offset'])
        if groupby == 'stage_id':
            grouped_applications = [Application_Id.concat(*g)
                                    for k, g in groupbyelem(applications,
                                                            itemgetter(
                                                                'stage_id'))]
        else:
            grouped_applications = [applications]

        values.update({
            'date': date_begin,
            'grouped_applications': grouped_applications,
            'page_name': 'application',
            'pager': pager,
            'default_url': '/my/applications',
            'searchbar_sortings': searchbar_sortings,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'groupby': groupby,
            'sortby': sortby,
            'filterby': filterby,
        })
        return request.render('cc_application.my_applications', values)


class Application(http.Controller):

    def _prepare_vals(self, post, model):
        values = {}
        fields = request.env['ir.model'].sudo().search([('model', '=', model)],
                                                       limit=1).field_id
        for key, val in post.items():
            field_id = fields.sudo().filtered(
                lambda r: r.sudo().name == key).sudo()
            if not field_id:
                continue
            if field_id.ttype == 'many2one':
                val = int(val) if val else False
            if field_id.ttype == "boolean":
                val = True if val == 'on' else False
            if field_id.ttype == "one2many":
                data = json.loads(val)
                val = [(0, 0, line) for line in data]
            values.update({
                key: val
            })
        return values

    @http.route(['/application'], type='http', auth="public", website=True)
    def grant_application(self, **post):
        if post:
            vals = self._prepare_vals(post, 'grant.application')
            vals.update({'country_id': 231})
            application_id = request.env['grant.application'].sudo().create(
                vals)
            superuser_id = request.env['res.users'].sudo().browse(SUPERUSER_ID)

            acknowledgement_mail = request.env.ref(
                'cc_application.acknowledgement_mail').sudo() if application_id.tier in (
            'Tier 1', 'Tier 2') \
                else request.env.ref(
                'cc_application.acknowledgement_mail_tier3').sudo()
            if acknowledgement_mail:
                acknowledgement_mail.with_context({
                                                      'email_from': request.env.company.email or superuser_id.email}).send_mail(
                    application_id.id, force_send=True)
                values = {
                    'body': acknowledgement_mail.body_html,
                    'model': 'grant.application',
                    'message_type': 'email',
                    'res_id': application_id.id,
                }
                request.env['mail.message'].with_user(
                    superuser_id).sudo().create(values)
            if application_id.tier in ('Tier 1', 'Tier 2'):
                user_vals = {
                    'name': application_id.your_name,
                    'login': application_id.email,
                    'email': application_id.email,
                }
                user_id = request.env['res.users'].sudo().create(user_vals)
                user_id.with_context({'create_user': 1,
                                      'email_from': superuser_id.email}).action_reset_password()

                internal_group_id = request.env.ref('base.group_user')
                portal_group_id = request.env.ref('base.group_portal')
                internal_group_id.sudo().users = [(3, user_id.id)]
                portal_group_id.sudo().users = [(4, user_id.id)]
                application_id.sudo().write({'user_id': user_id.id})
            else:
                eoi_group_users = request.env.ref(
                    'cc_application.group_eoi_user').sudo().users
                template_id = request.env.ref(
                    'cc_application.notification_email').sudo()
                base_url = request.env['ir.config_parameter'].sudo().get_param(
                    'web.base.url')
                action_id = request.env.ref(
                    'cc_application.action_grant_application').sudo()
                url = base_url + '/web#id=' + str(
                    application_id.id) + '&action=' + str(
                    action_id.id) + '&view_type=form&model=grant.application'
                ctx = {
                    'email_from': superuser_id.email,
                    'url': url,
                }
                for user in eoi_group_users:
                    ctx.update({
                        'email_to': user.email,
                        'user_name': user.name,
                    })
                    template_id.sudo().with_context(ctx).send_mail(
                        application_id.id, force_send=True)
                values = {
                    'body': template_id.body_html,
                    'model': 'grant.application',
                    'message_type': 'email',
                    'res_id': application_id.id,
                }
                request.env['mail.message'].with_user(
                    superuser_id).sudo().create(values)
                application_id.sudo().write({'stage_id': request.env.ref(
                    'cc_application.state_eoi').id})
            if application_id:
                return request.redirect('/thankyou')
        grant_types = request.env["grant.types"].sudo().search([], limit=1)
        project_location = grant_types.location_ids or []
        vals = {
            'grant_types': grant_types,
            'project_location': project_location,
        }
        return request.render("cc_application.application_detail_page", vals)

    @http.route(['/application/<model("res.country"):country>'], type='json',
                auth="user", methods=['POST'], website=True)
    def application_information(self, country, **kw):
        return dict(
            states=[(st.id, st.name, st.code) for st in country.state_ids],
            phone_code=country.phone_code,
            zip_required=country.zip_required,
            state_required=country.state_required,
        )

    @http.route(['/thankyou'], type='http', auth="public", website=True)
    def thankyou_postal(self, **post):
        return request.render("cc_application.thank_you_application")

    @http.route(['/application/proceed/'], type='http', auth="public",
                website=True)
    def application_proceed(self, **post):
        return request.render("cc_application.application_proceed")

    @http.route(['/application/declaration/'], type='http', auth="public",
                website=True)
    def application_declaration(self, **post):
        return request.render("cc_application.application_declaration")

    @http.route(['/application/privacy/'], type='http', auth="public",
                website=True)
    def application_privacy(self, **post):
        return request.render("cc_application.application_privacy")

    @http.route(['/application/edit/<int:application_id>'], type='http',
                auth="public", website=True)
    def application_edit(self, application_id, **post):
        values = {
            'application_id': request.env['grant.application'].browse(
                application_id),
        }
        return request.render("cc_application.application_main", values)

    @http.route(['/get/project_location/'], type='http', auth='public',
                website=True, csrf=False)
    def get_project_location(self, **post):
        vals = {}
        if post and post.get('grant_type') and post.get('post_code_value'):
            grant_type = request.env['grant.types'].sudo().browse(
                int(post.get('grant_type')))
            location_id = False
            for location in grant_type.location_ids:
                if post.get('post_code_value') in location.post_code_ids.mapped(
                        'name'):
                    location_id = location
                    break
            if location_id:
                vals.update({
                    'location_id': location_id.id,
                })
        return json.dumps(vals)

    # @http.route(['/get/project/'], type='http', auth='public', website=True, csrf=False)
    # def get_project(self, **post):
    #     vals = {}
    #     if post and post.get('project_id'):
    #         grant_application_id = request.env['grant.application'].sudo().search([('name', '=', post.get('project_id'))], limit=1)
    #         if grant_application_id:
    #             vals.update({
    #                 'project_name': grant_application_id and grant_application_id.project_name or '',
    #                 'project_description': grant_application_id and grant_application_id.project_description or '',
    #             })
    #     return json.dumps(vals)

    @http.route(['/get/grant_type/'], type='http', auth='public', website=True,
                csrf=False)
    def get_grant_type(self, **post):
        vals = {}
        if post and post.get('grant_type') and post.get('location'):
            grant_type_id = request.env["cc.grant.location"].sudo().search([
                ('location_id', '=', int(post.get('location'))),
                ('grant_type_id', '=', int(post.get('grant_type')))])
            vals = {
                'tier_one': grant_type_id.tier_one,
                'tier_two': grant_type_id.tier_two,
                'tier_three': grant_type_id.tier_three,
                'strategic_data': [{
                    'name': line.name,
                } for line in
                    grant_type_id.location_id.strategic_objective_ids],
                'headline_data': [{
                    'name': line.name,
                } for line in grant_type_id.location_id.headline_outputs_ids],
            }
        return json.dumps(vals)

    def _prepare_updation_vals(self, post, model):
        values = {}
        fields = request.env['ir.model'].sudo().search([('model', '=', model)],
                                                       limit=1).field_id
        for key, val in post.items():
            field_id = fields.sudo().filtered(
                lambda r: r.sudo().name == key).sudo()
            if not field_id:
                continue
            if field_id.ttype == 'binary':
                val = val.split('base64,')[1] if val else False
            if field_id.ttype == 'integer':
                val = int(val) if val else 0
            if field_id.ttype == 'selection':
                continue
            if field_id.ttype == 'many2one':
                val = int(val) if val else False
            if field_id.ttype == "boolean":
                val = True if val else False
            if field_id.ttype == "one2many":
                val = [(5, 0)] + [(0, 0, line) for line in val]
            values.update({
                key: val
            })
        return values

    @http.route('/application/save/', type='json', auth='user', website=False,
                csrf=False,
                Methods=['POST'])
    def application_save(self, **kw):
        vals = request.jsonrequest
        new = self._prepare_updation_vals(vals['params'], 'grant.application')
        application_id = request.env['grant.application'].browse(
            int(vals['params']['application_id']))
        application_id.write(new)
