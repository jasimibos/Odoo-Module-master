odoo.define("ibos_pos_item_count.order_line", function (require) {
    "use strict";
    var dict = {};
    var item_counter = 0;
    var total_qty = 0;
    require("point_of_sale.screens").OrderWidget.include({
        render_orderline: function (order_line) {
            var node = this._super.apply(this, arguments);
            item_counter = 0;
            total_qty = 0;
            var orderlines = order_line.order.orderlines.models;
            orderlines.forEach(function (order_line) {
                total_qty += order_line.quantity;
                item_counter++;
            });
            return node;
        },
        update_summary: function(){
            this._super();
            $(this.el).find('.item-count').html("<p>Total Item: <b style='color: red;'>" + item_counter + "</b>" + " Total QTY: <b style='color: red;'>" + total_qty + "</b></p>")
        },
        renderElement: function(){
            this._super();
            var order  = this.pos.get_order();
            if (!order) {
                return;
            }
            var orderlines = order.get_orderlines();
            if(orderlines.length == 0){
                item_counter = 0;
                total_qty = 0;
            }
        }
    });
})