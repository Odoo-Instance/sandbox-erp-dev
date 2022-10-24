odoo.define('pos_sale_receipt.pos_receipt', function(require) {
    "use strict";
    const models = require('point_of_sale.models');
    let _super_posmodel = models.PosModel.prototype;
    var _super_order = models.Order.prototype;
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    models.PosModel = models.PosModel.extend({
        // @Override
        _save_to_server: function (orders, options) {
            var self = this;
            var order_ids_to_sync = _.pluck(orders, 'id');
            return _super_posmodel._save_to_server.apply(this,arguments).then( function(server_ids){
                if (server_ids.length)
                {
                    var send_warning = Object.keys(server_ids[0]).includes('send_warning') ? server_ids[0]['send_warning'] : False
                    var remaining_sequence = Object.keys(server_ids[0]).includes('remaining_sequence_number') ? server_ids[0]['remaining_sequence_number'] : False
                    if (send_warning && remaining_sequence)
                    {
                        alert('Only '+ server_ids[0]['remaining_sequence_number'].toString() +' sequence left. Pos will stop once you reach ending sequence')
                    }
                }
                _.each(order_ids_to_sync, function (order_id) {
                    self.db.remove_order(order_id);
                });
                self.set('failed',false);
                return server_ids;
            }).catch(function (error){
                console.warn('Failed to send orders:', orders);
                if(error.code === 200 ){    // Business Logic Error, not a connection problem
                    // Hide error if already shown before ...
                    if ((!self.get('failed') || options.show_error) && !options.to_invoice) {
                        self.set('failed',error);
                        throw error;
                    }
                }
                throw error;
            });
        },
    });
});
