# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com
from dateutil.relativedelta import relativedelta

from odoo import api,fields , models , _

from datetime import date
from odoo import SUPERUSER_ID

RISK_SELECTION = [('High','High'),('Medium','Medium'),('Low','Low')]

class GrantApplicationState(models.Model):
    _name = 'grant.application.state'
    _description = 'Stages of Application'
    _order = 'sequence, name'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    description = fields.Text(string='Stage description', translate=True)
    sequence = fields.Integer('Sequence', default=1)
    fold = fields.Boolean(string='Folded in Kanban', default=False)

class GrantApplication(models.Model):
    _name = 'grant.application'
    _description = "Grant Application"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')

    def default_grant_type(self):
        return self.env['grant.types'].search([], limit=1)

    def _get_default_stage_id(self):
        return self.env['grant.application.state'].search([], limit=1)

    name = fields.Char(copy=False, readonly=True, index=True, default='New')
    business_name = fields.Char(string='Business Name', required=True)
    grant_types_id = fields.Many2one('grant.types', string='Grant Types', default=lambda s: s.default_grant_type())
    location_ids = fields.Many2many(related='grant_types_id.location_ids')
    project_location = fields.Many2one('cc.location', string="Project Location", required=True, domain="[('id', 'in', location_ids)]")
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    existing_project_details = fields.Text(string='Project Details')
    user_id = fields.Many2one('res.users', string='Users', copy=False)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    total_grant_requested = fields.Float(string="Total Grant Requested")
    planned_start_date = fields.Date(string="Planned Start Date", required=True)
    planned_end_date = fields.Date(string="Planned End Date", required=True)
    your_name = fields.Char(string="Your Name", required=True)
    email = fields.Char(string='Email', required=True)
    total_project_cost = fields.Float(string="Total Project Costs", compute='_compute_total_project_cost', store=True)
    phone = fields.Char(string='Phone', required=True)
    position = fields.Char(string='Position')
    stage_id = fields.Many2one('grant.application.state', ondelete='restrict', default=_get_default_stage_id, group_expand='_read_group_stage_ids', tracking=True, copy=False)
    is_eoi = fields.Boolean(compute="_get_stage_name")
    amount = fields.Monetary(string="Amount")
    tier = fields.Char(string="Tier",compute='_compute_tier', store=True)
    round_id = fields.Many2one('cc.round', domain="[('grant_type_id', '=', grant_types_id)]")
    is_previous_project = fields.Boolean(string="Existing project?")
    program = fields.Char(string="Which Project?")
    project_cost_ids = fields.One2many('cc.project.cost', 'project_cost_id', string='Porject Cost')
    headline_outputs_ids = fields.One2many('cc.headline.outputs', 'grant_application_id', string='Headline Outputs')
    alter_phone = fields.Char(string="Alternative Phone")
    secondary_contact_name = fields.Many2one('res.partner', string="Secondary Name")
    is_business_exist = fields.Boolean(string='Does the Business exist?')
    is_location_eligible = fields.Boolean(string='Is the location eligible?')
    is_cost_broadly_eligible = fields.Boolean(string='Are the costs broadly eligible?')
    is_eligible_limit = fields.Boolean(string='Is the Grant requested within eligible limits?')
    is_description_clear = fields.Boolean(string='Is the Project description is clear?')
    is_timesheet_real = fields.Boolean(string='Are the Timescales realistic?')
    is_strategic_fit_score = fields.Boolean(string='Does the Strategic Fit Score?')
    is_initial_vfm = fields.Boolean(string='Will the initial output deliver VFM?')
    is_all_checked = fields.Boolean(string='Is All Checked', compute='_compute_is_all_checked', store=True)
    eoi_score = fields.Char(string='EOI Score')

    board_decision_first_date = fields.Date(string='EOI Board Decision 1st Date')
    board_decision_type = fields.Selection([('Approved', 'Approved'), ('Rejected', 'Rejected'), ('More Info', 'More Info')], string='EOI Board Decision 1st')
    eoi_fail_note = fields.Text(string='First EOI Failed Note')
    eoi_acceptance_note = fields.Text(string='First Acceptance Note')

    board_decision_second_date = fields.Date(string='EOI Board Decision 2nd Date')
    board_decision_type_second = fields.Selection([('Approved', 'Approved'), ('Rejected', 'Rejected'), ('More Info', 'More Info')], string='EOI Board Decision 2nd')
    eoi_fail_note_second = fields.Text(string='Second EOI Failed Note')
    eoi_acceptance_note_second = fields.Text(string='Second Acceptance Note')

    last_user_updated_date = fields.Date('Last Updated Date by User itself.')

    # Project Fields
    project_name = fields.Char('Project Name', required=True)
    project_description = fields.Text(string="Project Description", required=True)
    project_overview = fields.Text(string="Project Overview")
    project_intend = fields.Text(string="Explaining what you want to do and how you intend to do it.")
    project_achieve = fields.Text(string="Why the project is needed and what it will achieve for your business.")
    eoi_notes = fields.Text(string="EOI Notes")
    eoi_attachments = fields.Many2many('ir.attachment', relation="m2m_eoi_rel", column1="m2m_eoi_id", column2="attachment_id", string="EOI Attachments")
    changes_notes = fields.Text(string="Changes Notes")
    changes_attachments = fields.Many2many('ir.attachment', relation="m2m_changes_rel", column1="m2m_changes_id", column2="attachment_id", string="Changes Attachments")

    # Strategic Fit Fields
    strategic_objective_ids = fields.One2many('cc.strategic.objectives', 'grant_application_id', string='Strategic Objectives')
    objectives_summary = fields.Text(string='Objectives Summary')
    outcomes_summary = fields.Text(string='Outcomes Summary')
    tip_objectives = fields.Text(string='How your project fits the call priorities set for the current round?')
    outsides_priority = fields.Text(string='If your business/activity falls outside?')

    # Project Options
    why_this_activity = fields.Text(string="Why have you chosen this particular activity?")
    not_procees = fields.Boolean(string="Project would not proceed")
    longer_timescale = fields.Boolean(string="Project may proceed but over a longer timescale")
    impact_on_quality = fields.Boolean(string="Project might proceed but at a lower level of quality and impact")
    proceed = fields.Boolean(string="We would still have sufficient funds to proceed")

    # contact details
    # contact_name = fields.Char(string="Name")
    # contact_email_address = fields.Char(string="Email")
    # contact_primary_telephone_number = fields.Char(string="Telephone")
    # contact_alternative_telephone_number = fields.Char(
    #     string="Alternative Telephone")
    contact_secondary_contact_name = fields.Char(string="Alternative Name")
    # contact_position_in_the_organisation = fields.Char(
    #     string="Position in Organisation")
    # contact details

    # organisation_details

    alternative_street = fields.Char()
    alternative_street2 = fields.Char()
    alternative_city = fields.Char()
    alternative_zip = fields.Char()
    alternative_state_id = fields.Many2one("res.country.state", string='State')
    alternative_country_id = fields.Many2one('res.country', string='Country')
    org_name = fields.Char()
    org_website = fields.Char()
    org_size = fields.Selection([('Micro 0-9 employees', 'Micro 0-9 employees'),
                                 ('Small 10-49 employees',
                                  'Small 10-49 employees'), (
                                 'Medium 50-249 employees',
                                 'Medium 50-249 employees'),
                                 ('large 250+', 'large 250+')
                                 ],
                                string='Business Size')
    org_type = fields.Many2one('cc.org.type')
    org_type_detail = fields.Text()
    sic_code = fields.Char()
    org_start_date = fields.Date()
    org_legal_status = fields.Selection(
        [('sole_trader', 'Sole Trader'), ('partnership', 'Partnership'),
         ('limited_liability_partnership', 'Limited Liability Partnership'),
         ('company_ltd_by_shares', 'Company ltd by shares'),
         ('company_ltd_by_guarantee', 'Company ltd by guarantee'),
         ('community_interest_company', 'Community Interest Company'),
         ('registered_charity', 'Registered Charity'), ('other', 'other')
         ],
        string='Business Size')
    org_utr = fields.Char()
    credit_check = fields.Binary(attachment=True)
    org_address = fields.Text()
    alternative_address_sel = fields.Boolean()
    org_alternative_address = fields.Char()
    org_alternative_address_data = fields.Text()
    fte_count = fields.Integer()
    org_house_no = fields.Integer()
    org_charity_no = fields.Integer()
    org_legal_about = fields.Text()
    org_vat = fields.Boolean()
    vat_reg_no = fields.Char()
    org_net_or_cost = fields.Selection([('gross', 'Gross'), ('net', 'Net')])
    org_gross_about = fields.Text()
    org_about = fields.Text()
    employee_male = fields.Integer()
    employee_female = fields.Integer()
    employee_gender_not_to_say = fields.Integer()
    employee_disable = fields.Integer()
    employee_not_disable = fields.Integer()
    employee_disability_not_to_say = fields.Integer()
    employee_16_24 = fields.Integer()
    employee_25_29 = fields.Integer()
    employee_30_34 = fields.Integer()
    employee_35_39 = fields.Integer()
    employee_40_45 = fields.Integer()
    employee_45_49 = fields.Integer()
    employee_50_54 = fields.Integer()
    employee_55_59 = fields.Integer()
    employee_60_64 = fields.Integer()
    employee_65 = fields.Integer()
    employee_age_not_to_say = fields.Integer()
    employee_white = fields.Integer()
    employee_mixed = fields.Integer()
    employee_multiple_ethnic_groups = fields.Integer()
    employee_asian_british = fields.Integer()
    employee_asian = fields.Integer()
    employee_black = fields.Integer()
    employee_african = fields.Integer()
    employee_caribbean = fields.Integer()
    employee_black_british = fields.Integer()
    employee_other_ethnic_group = fields.Integer()
    employee_cat_not_to_say = fields.Integer()
    share_holder_details_ids = fields.One2many('cc.shareholder.details',
                                               'share_holder_id',
                                               string='ShareHolder share Details')
    business_share_details_ids = fields.One2many('cc.business.share.details',
                                                 'business_details_id',
                                                 string='Business Share Details')
    share_holder_ids = fields.One2many('cc.shareholders',
                                       'shareholder_id',
                                       string='ShareHolder Details')
    
    
    #Deliverability
    deliverability_summary = fields.Text('Summary of how your project will be delivered, capacity and capability.')
    deliverability_process = fields.Text('Description of the systems and processes that will be used to ensure only costs directly related \
                                        to the project will be included in grant claims')
    deliverability_manage = fields.Text('Description how the project will be managed and governed')
    deliverability_experience = fields.Text('What experience does the organisation have of delivering this type of activity?')
    is_prev_funding = fields.Boolean('Have received Public Sector funding (Incl. EU, Local Authority, \
                                        Government Departments etc) previously?')
    previous_funding = fields.Text('Previous Funding')
    

    
    #Risks
    risk_ids = fields.One2many('cc.project.risk','application_id','Risks',default=lambda self: self._get_risks())

    #Timescales
    milestone_ids = fields.One2many('cc.milestone','application_id','Milestones')
    is_time_critical = fields.Boolean('Is Time Critical')
    time_critical = fields.Text('Time Critical Comment')

    # Subsidy Control
    is_other_funders = fields.Boolean()
    # provide_details = fields.Text()
    subsidy_control_summary_info = fields.Text()
    link_org = fields.Boolean()
    link_org_funding_body = fields.Text()
    link_org_activity = fields.Text()
    link_org_date_grant = fields.Date()
    link_org_currency = fields.Text()
    state_aid_report = fields.Binary(attachment=True)
    subsidy_control_details_ids = fields.One2many('cc.subsidy.control.details',
                                                 'subsidy_control_details_id',
                                                 string='Subsidy Control Details')

    # Permissions and Consent
    is_freehold_land = fields.Boolean()
    land_registry = fields.Binary(attachment=True)
    is_freeholder_permission = fields.Boolean()
    letter_consent = fields.Binary(attachment=True)
    is_plan_permission = fields.Boolean()
    plan_permission = fields.Binary(attachment=True)
    is_build_regulation = fields.Boolean()
    build_regulation = fields.Binary(attachment=True)
    other_permission = fields.Text()
    other_permission_attach = fields.Binary(attachment=True)

    # Benefits and Impacts
    wider_benefits_impact = fields.Text()
    reduction_local = fields.Boolean()
    improve_local = fields.Boolean()
    greater_capital = fields.Boolean()
    higher_quality = fields.Boolean()
    improve_pride = fields.Boolean()
    penzance_reduction_local = fields.Boolean()
    modern_local = fields.Boolean()
    improve_local_connectivity = fields.Boolean()
    penzance_greater_capital = fields.Boolean()
    streetscape = fields.Boolean()
    social_impact = fields.Text()
    market_increase = fields.Text()
    displacement_add_value = fields.Text()
    ensure_benefits = fields.Text()
    sustainability = fields.Text()
    
    #Declaration and Signature
    is_dq_director = fields.Boolean('Disqualified as a director')
    dq_director_desc = fields.Text('Disqualified as a director details')
    is_listed = fields.Boolean('Listed on the individual insolvency register')
    listed_desc = fields.Text('Listed on the individual insolvency register details')
    is_subject_bankruptcy = fields.Boolean('Subject to bankruptcy proceedings')
    subject_bankruptcy_desc = fields.Text('Subject to bankruptcy proceedings details')
    is_subject_county = fields.Boolean('Subject to a county court judgemen')
    subject_county_desc = fields.Text('Subject to a county court judgemen details')
    
    @api.model
    def _get_risks(self):
       vals = [(0, 0, {'name': 'Cost Increase'}),
               (0, 0, {'name': 'Supplier issues'}),
               (0, 0, {'name': 'Time overrun'}),
               (0, 0, {'name': 'Loss of key staff'}),
               ]
       return vals

    @api.depends('stage_id')
    def _get_stage_name(self):
        for rec in self:
            rec.is_eoi = True if rec.stage_id == self.env.ref('cc_application.state_eoi') else False

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return self.env['grant.application.state'].search([])

    def create_portal_user(self):
        self.ensure_one()
        user_vals = {
            'name': self.your_name,
            'login': self.email,
            'email': self.email,
        }
        user_id = self.env['res.users'].sudo().create(user_vals)
        internal_group_id = self.env.ref('base.group_user')
        portal_group_id = self.env.ref('base.group_portal')
        internal_group_id.sudo().users = [(3, user_id.id)]
        portal_group_id.sudo().users = [(4, user_id.id)]
        self.sudo().write({'user_id': user_id.id, 'stage_id': self.env.ref('cc_application.state_application').id})
        self._message_log(body=('User Created!'))

    def action_rejection(self):
        self.ensure_one()
        ctx = {
            'default_model': 'grant.application',
            'default_res_id': self.ids[0],
            'default_subject': 'Grant Application – Reference %s' % (self.name),
            'default_composition_mode': 'comment',
            "default_template_id": self.env.ref('cc_application.rejection_email').id,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_more_info(self):
        self.ensure_one()
        ctx = {
            'default_model': 'grant.application',
            'default_res_id': self.ids[0],
            'default_composition_mode': 'comment',
            "default_template_id": self.env.ref('cc_application.application_more_info').id,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_eoi_failed(self):
        self.ensure_one()
        ctx = {
            'default_model': 'grant.application',
            'default_res_id': self.ids[0],
            'default_subject': 'Grant Application – Reference %s' % (self.name),
            'default_composition_mode': 'comment',
            "default_template_id": self.env.ref('cc_application.application_eoi_failed').id,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    @api.depends('is_business_exist', 'is_location_eligible',
                'is_cost_broadly_eligible', 'is_eligible_limit',
                'is_description_clear', 'is_timesheet_real',
                'is_strategic_fit_score', 'is_initial_vfm')
    def _compute_is_all_checked(self):
        for record in self:
            if (record.is_business_exist and
                record.is_location_eligible and
                record.is_cost_broadly_eligible and
                record.is_eligible_limit and
                record.is_description_clear and
                record.is_timesheet_real and
                record.is_strategic_fit_score and
                record.is_initial_vfm and record.stage_id == self.env.ref('cc_application.state_eoi')):
                record.is_all_checked = True
            else:
                record.is_all_checked = False

    @api.depends('project_cost_ids', 'project_cost_ids.total_cost')
    def _compute_total_project_cost(self):
        for record in self:
            record.total_project_cost = sum(record.project_cost_ids.mapped('total_cost'))

    @api.depends('grant_types_id', 'total_grant_requested', 'project_location')
    def _compute_tier(self):
        for record in self:
            if record.grant_types_id and record.total_grant_requested and record.project_location:
                filter_grant_location = record.grant_types_id.grant_location_ids.filtered(lambda r: r.location_id.id == record.project_location.id)
                grant_location = filter_grant_location and filter_grant_location[0] or False
                if grant_location:
                    if record.total_grant_requested <= grant_location.tier_one:
                        record.tier = 'Tier 1'
                    elif record.total_grant_requested > grant_location.tier_one and record.total_grant_requested <= grant_location.tier_two:
                        record.tier = 'Tier 2'
                    elif record.total_grant_requested > grant_location.tier_one \
                        and record.total_grant_requested > grant_location.tier_two \
                        and record.total_grant_requested <= grant_location.tier_three:
                        record.tier = 'Tier 3'
                    else:
                        record.tier = 'No Tier'
                else:
                    record.tier = 'No Tier'
            else:
               record.tier = 'No Tier'

    @api.model
    def create(self, vals):
        # assigning the sequence for the record
        vals['name'] = self.env['ir.sequence'].next_by_code('grant.application.seq')
        vals['last_user_updated_date'] = date.today()
        res = super(GrantApplication, self).create(vals)
        if res.project_location and res.project_location.location_code:
            res.project_location.location_sequence += 1
            res.name = res.project_location.location_code + '-' + str(res.project_location.location_sequence).zfill(5)
        return res

    def print_eoi_document(self):
        return self.env.ref('cc_application.grant_application_report_template').report_action(self)

    def send_reminder_mail(self):
        # self.ensure_one()
        now_date = fields.Date.today()
        records = self.env['grant.application'].search([])
        for reg_rec in records:
            reg_date = reg_rec.create_date
            difference = relativedelta(reg_date, now_date)
            if difference.days == -4 and reg_rec.tier == "Tier 2" and reg_rec.email:
                if reg_rec.stage_id == self.env.ref('cc_application.state_registration'):
                    ctx = {
                        "default_model": "grant.application",
                        "default_res_id": reg_rec.id,
                        "default_template_id": self.env.ref('cc_application.email_template_grant_registration').id,
                        "default_composition_mode": "comment",
                    }
                    return {
                        "type": "ir.actions.act_window",
                        "view_mode": "form",
                        "res_model": "mail.compose.message",
                        "views": [(False, "form")],
                        "view_id": False,
                        "target": "new",
                        "context": ctx,
                    }

    def _auto_check_round_expiry(self):
        records = self.search([]).filtered(lambda r: r.stage_id == self.env.ref('cc_application.state_registration'))
        for rec in records:
            if rec.round_id and rec.round_id.enddate == date.today() + relativedelta(days=7):
                self.env.ref('cc_application.round_expiry_email').with_context\
                    ({'email_from': self.env['res.users'].sudo().browse(SUPERUSER_ID).email}).send_mail(rec.id, force_send=True)
            
            elif rec.round_id and rec.round_id.enddate < date.today():
                rec.stage_id = self.env.ref('cc_application.state_close').id
                rec.active = False

    def _auto_notify_reminder(self):
        records = self.search([]).filtered(lambda r: r.stage_id == self.env.ref('cc_application.state_eoi'))
        for rec in records:
            if rec.last_user_updated_date and (date.today() - rec.last_user_updated_date).days == 30:
                self.env.ref('cc_application.reminder_30_days').with_context\
                    ({'email_from': self.env['res.users'].sudo().browse(SUPERUSER_ID).email}).send_mail(rec.id, force_send=True)

            elif rec.last_user_updated_date and (date.today() - rec.last_user_updated_date).days == 60:
                self.env.ref('cc_application.reminder_60_days').with_context\
                    ({'email_from': self.env['res.users'].sudo().browse(SUPERUSER_ID).email}).send_mail(rec.id, force_send=True)
                rec.active = False


class CcProjectCost(models.Model):
    _name = 'cc.project.cost'
    _description = 'Cc Project Post'

    project_cost_id = fields.Many2one('grant.application', string="Project Cost")
    expenditure = fields.Char(string="Expenditure Item")
    total_cost = fields.Monetary(string="Cost")
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(related='company_id.currency_id')



class CcShareholderdetails(models.Model):
    _name = 'cc.shareholder.details'
    _description = 'CcShareholderdetails'

    share_holder_id = fields.Many2one('grant.application',
                                      string="Share Holder")
    share_holder_name = fields.Char()
    company_reg_no = fields.Integer()
    share_in_percentage = fields.Float()
    no_of_employees = fields.Integer()
    comment = fields.Text()


class CcBusinessSharedetails(models.Model):
    _name = 'cc.business.share.details'
    _description = 'CcBusinessSharedetails'

    business_details_id = fields.Many2one('grant.application',
                                      string="Share Holder")
    share_holder_name = fields.Char()
    company_reg_no = fields.Integer()
    share_in_percentage = fields.Float()
    no_of_employees = fields.Integer()
    comment = fields.Text()

class CcShareHolderids(models.Model):
    _name = 'cc.shareholders'
    _description = 'CcSharedetails'

    shareholder_id = fields.Many2one('grant.application',
                                      string="Share Holder")
    share_holder_name = fields.Char()
    share_in_percentage = fields.Float()
    comment = fields.Text()

class CcSubsidyControldetails(models.Model):
    _name = 'cc.subsidy.control.details'
    _description = 'CcSubsidyControldetails'

    subsidy_control_details_id = fields.Many2one('grant.application',
                                      string=" Subsidy Control Details")
    
    funding_body = fields.Text()
    timescale = fields.Text()
    funding_required = fields.Text()
    project_desc = fields.Text()
    progress_update = fields.Text()


class CcProjectRisk(models.Model):
    _name = 'cc.project.risk'
    
    application_id = fields.Many2one('grant.application')
    name = fields.Char('Name')
    likelihood = fields.Selection(RISK_SELECTION,string="Likelihood")
    impact_severity = fields.Selection(RISK_SELECTION,string="Impact Severity")
    impact_description = fields.Char('(Tier 2& 3 only) How would the impact affect the project/your business?')
    mitigation = fields.Char('Mitigation')

class CcMilestone(models.Model):
    _name = 'cc.milestone'
    
    application_id = fields.Many2one('grant.application')
    milestone_name = fields.Char('Milestone')
    milestone_date = fields.Date('Date Achieved by')
    practical_completion = fields.Char('Practical Completion')
    practical_date = fields.Date('Date Achieved by')