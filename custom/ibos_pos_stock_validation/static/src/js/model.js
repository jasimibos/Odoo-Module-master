odoo.define('ibos_pos_stock_validation.models',function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    var gui = require('point_of_sale.Gui');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var _t  = require('web.core')._t;
    var session = require('web.session');

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var product_model = _.find(this.models, function (model) {
                return model.model === 'product.product';
            });
            product_model.fields.push('qty_available');

            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });

    var _super_orderline = models.Orderline;
        models.Orderline = models.Orderline.extend({

        get_product_quantity: function () {
            if (this.get_product_quantity) {
                return this.get_product_quantity
            }
            var product_quantity = this.product.qty_available;
            return product_quantity;
        }

    });

});