odoo.define('pos_order_summary_report.PaymentScreen', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {
        //@Override
        constructor() {
            super(...arguments);
            if(this.env.pos.config.auto_invoice) {
                this.currentOrder.set_to_invoice(true);
            }
        }
        };

    Registries.Component.extend(PaymentScreen, PosPaymentScreen);

    return PaymentScreen;
});
