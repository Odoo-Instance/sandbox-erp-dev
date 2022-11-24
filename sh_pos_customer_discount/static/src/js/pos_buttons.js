odoo.define('sh_pos_customer_discount.DiscountButton', function(require) {
'use strict';
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   const PaymentScreen = require('point_of_sale.PaymentScreen');


   class DiscountButton extends PosComponent {
        constructor() {
        super(...arguments);
        //useListener('click', this.onClick);
        }
        //Generate popup
      display_discount_popup() {
      var core = require('web.core');
      var _t = core._t;
       Gui.showPopup("DiscountPopup", {
       title : _t("Discount"),
       confirmText: _t("Exit")
          });
      }

        is_available() {

        const order = this.env.pos.get_order();

        return order

        }
   }

   DiscountButton.template = 'DiscountButton';
   ProductScreen.addControlButton({
        component: DiscountButton,
        condition: function() {
        return this.env.pos;
        },

   });

Registries.Component.add(DiscountButton);
   return DiscountButton;
});