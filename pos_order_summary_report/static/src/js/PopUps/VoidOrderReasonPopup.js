odoo.define(
  "pos_order_summary_report.VoidOrderReasonPopup",
  function (require) {
    "use strict";

    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");
    const Registries = require("point_of_sale.Registries");
    const { _lt } = require("@web/core/l10n/translation");
    var { Gui } = require("point_of_sale.Gui");

    class VoidOrderReasonPopup extends AbstractAwaitablePopup {
      constructor() {
        super(...arguments);
      }
      async VoidOrder(ev) {
        window.location.reload()
        var self = this;
        var void_reasons_ids = new Array();
        var inputElements = document.getElementsByClassName("void_reason");
        for (var i = 0; inputElements[i]; ++i) {
          if (inputElements[i].checked) {
            void_reasons_ids.push(parseInt(inputElements[i].id));
          }
        }
        if ($("#addition_reason_to_void").val()) {
          const new_void_order_reason_id = await this.rpc({
            model: "void.order.reason",
            method: "create",
            args: [[{ name: $("#addition_reason_to_void").val() }]],
          });
          void_reasons_ids.push(new_void_order_reason_id[0]);
        }
        debugger;
        const pos_order_void = await this.rpc({
          model: "pos.order",
          method: "void_order",
          args: [this.env.pos.current_order, [[6, 0, void_reasons_ids]]],
        }).then(function () {
          // window.location.reload();
        });
        this.props.resolve({ confirmed: false, payload: null });
        this.trigger("close-popup");
      }
    }
    VoidOrderReasonPopup.template = "VoidOrderReasonPopup";
    VoidOrderReasonPopup.defaultProps = {
      confirmText: _lt("Void Order"),
      cancelText: _lt("Cancel"),
    };

    Registries.Component.add(VoidOrderReasonPopup);

    return VoidOrderReasonPopup;
  }
);
