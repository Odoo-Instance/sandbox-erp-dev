odoo.define('pos_order_summary_report.VoidOrderPopup', function(require) {
    'use strict';

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { _lt } = require('@web/core/l10n/translation');
    var { Gui } = require('point_of_sale.Gui');
    var core = require('web.core');
    var _t = core._t;
    var models = require('point_of_sale.models');
    const session = require('web.session');

    // formerly ConfirmPopupWidget
    models.load_fields('res.users',['pos_security_pin']);
    
    class VoidOrderPopup extends AbstractAwaitablePopup {
    VoidOrder() {
        this.props.resolve({ confirmed: false, payload: null });
        this.trigger('close-popup');
    }
    async openVoidOrderReasonPopup() {
		/*added the password pop screen*/
		const { confirmed, payload } = await Gui.showPopup('NumberPopup', {
				title: _t('Password Required'),
				isPassword: true,
				confirmed: true,
			});
		if (confirmed){
				/*checked the current user*/
				let userPwd;
				var user = this.env.pos.user;
				for (let i = 0; i < this.env.pos.users.length; i++) {
					if (this.env.pos.users[i].id === user.id) {
						userPwd = this.env.pos.users[i].pos_security_pin;
					}
				}
				if (payload == userPwd){
					const {confirmed, payload } = await Gui.showPopup('VoidOrderReasonPopup', {
			            title: this.env._t('Reasons to void the order'),
			            body: this.env._t(
			                'what are the reasons to void this order?'
			            ),
			            //void_reasons : reasons,
			        });
				}else{
					Gui.showPopup('ErrorPopup', {
						title: _t('Invalid Password'),
						body: _t('Wrong Password'),
					});
					return false;
				}
        }
    }
    }
    VoidOrderPopup.template = 'VoidOrderPopup';
    VoidOrderPopup.defaultProps = {
        confirmText: _lt('Yes'),
        cancelText: _lt('No'),
    };

    Registries.Component.add(VoidOrderPopup);

    return VoidOrderPopup;
});
