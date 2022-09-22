odoo.define('awb_l10n_ph_pos.OrderRecieptPosProvider', function (require) {
    'use strict'
    const models = require('point_of_sale.models');
    models.load_fields('res.company', 
        ['awb_pos_provider_id',
        'awb_pos_provider_tin',
        'awb_pos_provider_accreditation_no',
        'awb_pos_provider_display_date',
        'awb_pos_provider_display_valid_until',
        'awb_pos_provider_ptu',
        'awb_pos_provider_remarks',
        'awb_pos_provider_display_address',]);
});