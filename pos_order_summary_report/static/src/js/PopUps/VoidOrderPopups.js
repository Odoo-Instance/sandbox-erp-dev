odoo.define('pos_order_summary_report.VoidOrderPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _lt } = require('@web/core/l10n/translation');
    var { Gui } = require('point_of_sale.Gui');

    // formerly ConfirmPopupWidget
    class VoidOrderPopup extends AbstractAwaitablePopup {
    VoidOrder() {
        this.props.resolve({ confirmed: false, payload: null });
        this.trigger('close-popup');
    }
    async openVoidOrderReasonPopup() {
        const reasons = await this.rpc({
            model: 'void.order.reason',
            method: 'search_read',
            fields: ['id', 'name'],
            domain: [],
        });
        const { confirmed } = await this.showPopup('VoidOrderReasonPopup', {
            title: this.env._t('Reasons to vois the order'),
            body: this.env._t(
                'what are the reasons to void this order?'
            ),
            void_reasons : reasons,
        });
    }
    }
    VoidOrderPopup.template = 'VoidOrderPopup';
    VoidOrderPopup.defaultProps = {
        confirmText: _lt('Void Order'),
        cancelText: _lt('Cancel'),
    };

    Registries.Component.add(VoidOrderPopup);

    return VoidOrderPopup;
});
