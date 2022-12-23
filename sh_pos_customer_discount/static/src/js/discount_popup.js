/** @odoo-module **/
   import AbstractAwaitablePopup from 'point_of_sale.AbstractAwaitablePopup';
   import Registries from 'point_of_sale.Registries';
   import PosComponent from 'point_of_sale.PosComponent';
   import ControlButtonsMixin from 'point_of_sale.ControlButtonsMixin';
   import NumberBuffer from 'point_of_sale.NumberBuffer';
   import { useListener } from 'web.custom_hooks';
   import { onChangeOrder, useBarcodeReader } from 'point_of_sale.custom_hooks';
   const { useState } = owl.hooks;
   const ProductScreen = require('point_of_sale.ProductScreen');
   
   /*extended the product screen to set the taxes for vat output*/
   const clickProductScreen = (ProductScreen) =>
		class extends ProductScreen {
			constructor() {
				super(...arguments);
			}
		
		async _clickProduct(event) {
            if (!this.currentOrder) {
                this.env.pos.add_new_order();
            }
            const product = event.detail;
            const options = await this._getAddProductOptions(product);
            // Do not add product if options is undefined.
            if (!options) return;
            if (product.taxes_id[0] == 2){
	            for (let k = 0; k < product.pos.taxes.length; k++) {
					if (product.pos.taxes[k].name == 'VAT (Output VAT)') {
						product.taxes_id[0] = product.pos.taxes[k].id
					}
				}
			}
            // Add the product after having the extra information.
            await this.currentOrder.add_product(product, options);
            NumberBuffer.reset();
        }
		
	};
	Registries.Component.extend(ProductScreen, clickProductScreen);
   
   
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
						/*changed the the tax type based on customer*/
						for (let k = 0; k < orderline.pos.taxes.length; k++) {
							if (orderline.pos.taxes[k].name == 'VAT - Exempt') {
								orderline.product.taxes_id[0] = orderline.pos.taxes[k].id
							}
						}
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
