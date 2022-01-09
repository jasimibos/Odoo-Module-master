odoo.define('ibos_pos_management.pos_order_screen', function (require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var order_count = require('ibos_pos_item_count.order_line')

    screens.ReceiptScreenWidget.include({
        get_receipt_render_env: function() {
            var node = this._super.apply(this, arguments);
            var mrp = [];
            var product_ids = []
            var get_products = []
            var order_lines = node['order'].get_orderlines()
            node.mrp = []

            for(var i in order_lines){
                product_ids.push(order_lines[i]['product']['product_tmpl_id'])
            }

            var mrp = rpc.query({
               model: 'product.template',
               method: 'get_ordered_products_mrp',
               args: [product_ids],
            }).then(function (result) {
                console.log("result return", result)
                for(var i in node['orderlines']){
                    console.log("Before result loop, current product name", node['orderlines'][i]['product']['display_name'], " and id is,",node['orderlines'][i]['product']['product_tmpl_id'])
                    for(var j in  result){
                        if(result[j]['id'] == node['orderlines'][i]['product']['product_tmpl_id']){
                            node['receipt']['orderlines'][i].mrp = result[j]['mrp']
                            console.log("Product id in orderlist ", node['orderlines'][i]['product']['product_tmpl_id'])
                            console.log("id in result ",result[j]['id']," mrp is result ", result[j]['mrp'])
                            node.mrp.push(result[j]['mrp'])
                        }
                        else{
                            node['receipt']['orderlines'][i].mrp = 0.0
                            node.mrp.push(0.0)
                        }
                    }
                }
                return node
           }).catch(function () {
               console.log("NO DATA");
           });

           return node
        },

    });

});
