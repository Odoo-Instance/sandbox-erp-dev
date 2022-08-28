# Copyright (C) 2022-TODAY CoderLab Technology Pvt Ltd
# https://coderlabtechnology.com

{
    'name': 'Grant Application',
    'category': 'Hidden',
    'summary': 'Grant Application module for helpdesk modules using the website',
    "license": "LGPL-3",
    'description': """
        Grant Application module for helpdesk modules using the website.  
        """,
    'depends': [
        'auth_signup',
        "portal",
        "web",
        'website',
    ],
    'data': [
        'security/ir.model.access.csv',
        "security/security.xml",
        'data/data.xml',
        'data/ir_sequence.xml',
        'data/base_automation.xml',
        'data/grant_sequence.xml',
        "data/mail_template.xml",
        'views/grant_application_views.xml',
        'views/application_template_view.xml',
        'views/thankyou_application.xml',
        'views/grant_type_views.xml',
        "views/application_proceed_views.xml",
        'views/application_declaration_views.xml',
        'views/application_privacy_views.xml',
        'views/cc_locations_views.xml',
        "views/webclient_templates.xml",
        'views/main_application.xml',
        'views/website_section.xml',
        'views/application_sections.xml',
        'views/cc_org_type.xml',
        # 'views/cc_postcodes_views.xml',
        'report/grant_application.xml',
        'report/grant_application_template.xml',
    ],

    'auto_install': True,
    'assets': {
        'web.assets_backend': [
            'cc_application/static/src/scss/application.scss',
        ],
        'web.assets_frontend': [
            'cc_application/static/src/js/custom.js',
            'cc_application/static/src/js/custom2.js',
            'cc_application/static/src/js/form.js',
            'cc_application/static/src/scss/style.scss',
        ],
    }
}
