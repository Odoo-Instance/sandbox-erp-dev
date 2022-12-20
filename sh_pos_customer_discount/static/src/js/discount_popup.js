/** @odoo-module **/
   import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
   import Registries from 'point_of_sale.Registries';
   import PosComponent from 'point_of_sale.PosComponent';
   import ControlButtonsMixin from 'point_of_sale.ControlButtonsMixin';
   import NumberBuffer from 'point_of_sale.NumberBuffer';
   import { useListener } from 'web.custom_hooks';
   import { onChangeOrder, useBarcodeReader } from 'point_of_sale.custom_hooks';
   const { useState } = owl.hooks;
   class DiscountPopup extends AbstractAwaitablePopup {
    constructor() {

    super(...arguments);
     this.state = useState({discountData:{discount:20}});
    //useListener('click-product', this._clickProduct);
    }

     get currentOrder() {
           return this.env.pos.get_order();
       }


       async confirm() {
        var discount = this.state.discountData['discount'];
            var selectedPartner = this.env.pos.get_order().get_client()
            if (selectedPartner != null) {
            if (selectedPartner.check_sc_pwd) {
				 _.each(this.env.pos.get_order().get_orderlines(), function (orderline) {
                    if (orderline) {
                        orderline.set_discount(discount)
                    }
            	});
            	this.props.resolve({ confirmed: true });
                this.trigger('close-popup');
			} else {
				this.showPopup('ConfirmPopup', {
		                        title: this.env._t('Alert'),
		                        body: this.env._t('Selected customer has no SC/PWD.'),
		                    }); 
			}
			} else {
				this.showPopup('ConfirmPopup', {
		                        title: this.env._t('Alert'),
		                        body: this.env._t('Please select the customer'),
		                    }); 
			}

       }
        captureChange(event){
            this.state.discountData[event.target.name] = event.target.value;
        }
    }
    //Create products popup
   DiscountPopup.template = 'DiscountPopup';
   DiscountPopup.defaultProps = {
       confirmText: 'Ok',
       cancelText: 'Cancel',
       title: 'Discount',
       body: '',
   };
   Registries.Component.add(DiscountPopup);
//   return DiscountPopup;
   export default  DiscountPopup;
