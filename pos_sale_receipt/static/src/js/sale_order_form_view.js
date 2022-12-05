odoo.define('pos_sale_receipt.FormView', function (require) {
    "use strict";
    var FormController = require('web.FormController');
    var ExtendFormController = FormController.include({
         _saveRecord: function () {
            if(this.modelName == 'sale.order'){
                var record = this.model.get(this.handle, {raw: true});
                var team_id = record["data"]["team_id"]
                var show_warning = record["data"]["show_warning"]
                var remaining_receipts = record["data"]["remaning_receipts_count"]
                if (team_id && show_warning && remaining_receipts > 0){
                    alert("Only "+ remaining_receipts.toString() + " receipts number left")
                }
            }
            return this._super.apply(this, arguments);
        },

    });
});
    