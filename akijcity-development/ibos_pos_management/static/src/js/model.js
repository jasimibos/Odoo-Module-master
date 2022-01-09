odoo.define('ibos_pos_management.pos_order_barcode', function (require) {
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

            if (res['uid'].split('-').length > 0){
                var order_codes = res['uid'].split('-')
                var order_ref = ""
                for(var i in order_codes){
                    order_ref += order_codes[i]
                }
                res['name'] = _.str.sprintf(_t("%s"), order_ref);
            }
            else{
                res['name'] = _.str.sprintf(_t("%s"), res['uid']);
            }
            return res
        },

    });

});
