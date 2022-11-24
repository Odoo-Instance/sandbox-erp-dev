odoo.define("pos_order_summary_report.pos", function (require) {
  "use strict";

  var models = require('point_of_sale.models');
  models.load_models([{
        model: 'pos.order',
        fields: ['id', 'name', 'void_reason_ids'],
        loaded: function(self,orders){
            self.orders = orders;
            debugger;
            console.log("order---", orders);
            if(orders.length)
            {
              self.current_order = orders[0].id + 1;
            }
            else{
              self.current_order = 1
            }
             },
     }]);

});
