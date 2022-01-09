odoo.define('ibos_pos_item_count.product_and_quantity_count', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    screens.ReceiptScreenWidget.include({
        get_receipt_render_env: function() {
            var node = this._super.apply(this, arguments);
            var order_lines = node['order'].get_orderlines()
            var total_products = order_lines.length
            var total_Qtys = 0.0

            for(var i in order_lines){
                total_Qtys += order_lines[i]['quantity']
            }
            node.total_products = total_products
            node.total_Qtys = total_Qtys

            return node
        },

    });

});
