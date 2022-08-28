# -*- coding: utf-8 -*-
{
    "name": """Theme Backend""",
    "summary": """This module change a backend theme.""",
    "category": "CC Backend Theme",
    "author": "Mohit Nakrani",
    "maintainer": "Mohit Nakrani",
    "support": "mohitnakrani123@gmail.com",
    "license": "LGPL-3",
    "depends": ["web", "web_enterprise"],
    "external_dependencies": {"python": [], "bin": []},
    "data": [
    ],
    'assets': {
        'web._assets_primary_variables': [
            'cc_theme_backend/static/src/scss/theme_style.scss',
        ],
    },
    "demo": [],
    "qweb": [],
    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,
    "uninstall_hook": None,
    "auto_install": False,
    "installable": True,
}
