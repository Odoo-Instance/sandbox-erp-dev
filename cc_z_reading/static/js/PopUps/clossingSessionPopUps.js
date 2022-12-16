odoo.define('cc_z_reading.ClosePosPopup', function (require) {
    'use strict';

    const ClosePosPopup = require('point_of_sale.ClosePosPopup');
    const Registries = require('point_of_sale.Registries');

    const PosBlackboxBeClosePopup = (ClosePosPopup) =>
        class extends ClosePosPopup {
            async closeSession() {
                    let response;
                     response = await this.rpc({
                                        model: 'pos.session',
                                        method: 'clossing_session_report',
                                        args: [this.env.pos.pos_session.id],
                                        kwargs: {

                                        }
                                    })
                window.location = response.url;
                return super.closeSession();
            }
        };

    Registries.Component.extend(ClosePosPopup, PosBlackboxBeClosePopup);

    return ClosePosPopup;
});