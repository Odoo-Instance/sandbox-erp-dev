odoo.define('pos_order_summary_report.ReceiptScreen', function (require) {
    'use strict';

    const ReceiptScreen = require('point_of_sale.ReceiptScreen');
    const Registries = require('point_of_sale.Registries');
    console.log('file---------');

    const ReceiptScreenVoidOrder = ReceiptScreen =>
        class extends ReceiptScreen {
            cancel() {
                this.props.resolve({ confirmed: false, payload: null });
                this.trigger('close-popup');
            }
            async voidOrder() {
                const { confirmed } = await this.showPopup('VoidOrderPopup', {
                    title: this.env._t('Void this order'),
                    body: this.env._t(
                        'are you sure do you want to void this order?'
                    ),
                });
            }
        };

    Registries.Component.extend(ReceiptScreen, ReceiptScreenVoidOrder);

    return ReceiptScreen;

});
