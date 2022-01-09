odoo.define("ibos_pos_stock.pos_stock", function(require){
    "use strict";
    var core = require("web.core");
    var gui = require("point_of_sale.gui");
    var models = require("point_of_sale.models");
    var PosDb = require("point_of_sale.DB");
    var utils = require("web.utils");
    var screens = require("point_of_sale.screens");
    var rpc = require("web.rpc");
    var chrome = require("point_of_sale.chrome");
    var gui = require("point_of_sale.gui");
     var _t = core._t;

    screens.PaymentScreenWidget.include({
       validate_order: function (force_validation){
           var self = this;
           var _super = this._super;
           if(this.pos.config.allow_order_out_of_stock){
               return this._super(force_validation);
           }
           var order = this.pos.get_order();
           var orderlines = order.get_orderlines();
           var allow_order = true;
           for (var i = 0; i < orderlines.length; i++){
               var line = orderlines[i];
               if(line.product.type == "product" && line.product.qty_available < line.quantity){
                   console.log("lal")
                   allow_order = false;
                   this.gui.show_popup("error",{
                       title: _t("Order has out-of-stock product"),
                       body: _t(
                           "Product out of stock"
                       ),
                       do_not_change_cashier: true,
                       arguments: {ask_untill_correct:true},
                   });
                   return;
               }
           }
           if(allow_order){
               this._super(force_validation);
           }
       },
    });

    screens.ProductListWidget.include({
        init: function(parent, options) {
            var self = this;
            this._super(parent, options);
            if (this.pos.config.allow_order_out_of_stock) {
                return;
            }

            var click_product_handler_super = this.click_product_handler;
            this.click_product_handler = function() {
                var product = self.pos.db.get_product_by_id(this.dataset.productId);
                if (product.type === "product" && product.qty_available <= 0) {
                    return self.gui.show_popup("alert", {
                        title: _t("The product is out of stock"),
                        body: _t("It's unavailable to add the product"),
                    });
                }
                _.bind(click_product_handler_super, this)();
            };
        },
    });
});