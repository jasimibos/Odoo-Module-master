/*
    License: OPL-1
    author: farooq@aarsol.com   
*/
odoo.define('ibos_pos_invoce_receipt.order', function (require) {
    "use strict";

    var utils = require('web.utils');
    var round_pr = utils.round_precision;
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var qweb = core.qweb;
    var _t = core._t;

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            var res = _super_Order.initialize.apply(this, arguments);
            return res
        },      
        
        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            if (json.ean13) {
                this.ean13 = json.ean13;
            }
            return res;
        },
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            
            if (this.ean13) {
                json.ean13 = this.ean13;
            }
            if (!this.ean13 && this.uid) { // init ean13 and automatic create ean13 for order
                var ean13 = '';
                // if (this.pos.user.id) {
                //     ean13 += this.pos.user.id;
                // }
                // if (this.sequence_number) {
                //     ean13 += this.sequence_number;
                // }
                // if (this.pos.config.id) {
                //     ean13 += this.pos.config.id;
                // }
                var fean13 = this.uid.split('-');
                for (var i in fean13) {
                    ean13 += fean13[i];
                }

                ean13 = ean13.split("");

                var aean13 = []
                var sean13 = ""
                for (var i = 0; i < ean13.length; i++) {
                    if (i <= 12) {
                        sean13 += ean13[i]
                        aean13.push(ean13[i])
                    }
                }
                // this.ean13 = sean13 + this.generate_ean13(aean13).toString()
                this.ean13 = sean13
            }
            return json;
        },

        fix_tax_included_price: function (line) {
            _super_Order.fix_tax_included_price.apply(this, arguments);
            if (this.fiscal_position) {
                var unit_price = line.product['list_price'];
                var taxes = line.get_taxes();
                var mapped_included_taxes = [];
                _(taxes).each(function (tax) {
                    var line_tax = line._map_tax_fiscal_position(tax);
                    if (tax.price_include && tax.id != line_tax.id) {

                        mapped_included_taxes.push(tax);
                    }
                })
                if (mapped_included_taxes.length > 0) {
                    unit_price = line.compute_all(mapped_included_taxes, unit_price, 1, this.pos.currency.rounding, true).total_excluded;
                    line.set_unit_price(unit_price);
                }
            }
        },
        // Over write method
        generate_unique_id: function() {
        // Generates a public identification number for the order.
        // The generated number must be unique and sequential. They are made 12 digit long
        // to fit into EAN-13 barcodes, should it be needed

            function zero_pad(num,size){
                var s = ""+num;
                while (s.length < size) {
                    s = "0" + s;
                }
                return s;
            }
            var order_code =  zero_pad(this.pos.pos_session.id,5) +'-'+
                              zero_pad(this.pos.pos_session.login_number,3) +'-'+
                              zero_pad(this.sequence_number,4);

            var ean13 = '';
            var fean13 = order_code.split('-');
                for (var i in fean13) {
                    ean13 += fean13[i];
                }
            ean13 = ean13.split("");
            var aean13 = []
            var sean13 = ""
            for (var i = 0; i < ean13.length; i++) {
                if (i < 12) {
                    sean13 += ean13[i]
                    aean13.push(ean13[i])
                }
            }

            order_code = order_code + this.generate_ean13(aean13).toString()

            console.log("new order number ref is,", order_code)
            return order_code
        },


        generate_ean13: function (code) {
            if (code.length != 12) {
                return -1
            }
            var evensum = 0;
            var oddsum = 0;
            for (var i = 0; i < code.length; i++) {
                if ((i % 2) == 0) {
                    evensum += parseInt(code[i])
                } else {
                    oddsum += parseInt(code[i])
                }
            }
            var total = oddsum * 3 + evensum
            return parseInt((10 - total % 10) % 10)
        },
        
        
        
        get_total_before_tax: function() {
		    return this.get_total_without_tax() + this.get_order_discount();
		},
		get_order_discount: function() {
			return round_pr(this.orderlines.reduce((function(sum, orderLine) {
				if (orderLine.get_product().display_name == 'Discount Product')
					return sum + Math.abs(orderLine.get_price_without_tax());
				else
				    return sum;
			}), 0), this.pos.currency.rounding);
		},
       
        
        
    });

    var _super_Orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        
        get_item_discout: function(){
        	var discount = this.get_unit_price() * (this.get_discount() / 100.0);
        	return discount;        	
        },
        get_price_discount: function () { 
            var price_unit = this.get_unit_price();
            var prices = this.get_all_prices();
            var priceWithTax = prices['priceWithTax'];
            var tax = prices['tax'];
            var discount = priceWithTax - tax - price_unit;
            return discount
        },
        
    });
});
