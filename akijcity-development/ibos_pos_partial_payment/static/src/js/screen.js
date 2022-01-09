odoo.define('ibos_pos_partial_payment.order', function (require) {

    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var ScreenWidget = screens.ScreenWidget;
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var QWeb = core.qweb;
    var PopupWidget = require('point_of_sale.popups');
    var rpc = require('web.rpc');
    var _t = require('web.core')._t;
    var session = require('web.session');


    screens.PaymentScreenWidget.include({
        init: function (parent, options) {
            var self = this;
            this._super(parent, options);
            this.due = "";
            this.emp_id = 0;
        },

        // renderElement: function () {
        //     var self = this;
        //     this._super();
        //     console.log("calling Payment Lines from renderElement method from due payment module and see payments amount and due")
        //     var order = this.pos.get_order();
        //     var lines = order.get_orderlines();
        //     var extradue = this.compute_extradue(order);
        //     console.log("extradue ", extradue)
        //     console.log("pos Oder  ", order)
        //     var employee = this.pos.get_client()
        // },
        show: function () {
            var self = this;
            this._super();

            // var emp = this.pos.employees

            var employee = this.pos.get_client()

            if (employee) {
                if (employee["employess_id"]) {
                    this.emp_id = employee["employess_id"];
                    this.show_credit_button();

                } else {
                    this.hide_credit_button();
                }
            } else {
                this.hide_credit_button();
            }

        },
        hide_credit_button: function () {
            $(".partial-payment").hide();
        },

        show_credit_button: function () {
            $(".partial-payment").show();
        },
        render_paymentlines: function () {
            var self = this;
            this._super();
            var order = this.pos.get_order();
            // var extradue = this.compute_extradue(order);
            // console.log("extradue ",extradue)
            order.set_due(order.get_due())
        }

    });

    var _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({

        initialize: function (attributes, options) {
            _super_Order.initialize.apply(this, arguments);
            var self = this;
            options = options || {};
            this.amount_due = '';

        },
        set_due: function (due) {
            this.amount_due = due
        },
        // get_due: function () {
        //     return this.amount_due
        // },

        init_from_JSON: function (json) {
            var res = _super_Order.init_from_JSON.apply(this, arguments);
            // console.log("init from: ", this.amount_due)
            this.amount_due = json.amount_due;
            return res;
        },
        export_as_JSON: function () {
            var json = _super_Order.export_as_JSON.apply(this, arguments);
            // console.log("export from: ", this.amount_due)
            json.amount_due = this.amount_due;
            return json;
        },
    });

    models.PosModel.extend({
        _save_to_server: function (orders, options) {
            if (!orders || !orders.length) {
                var result = $.Deferred();
                result.resolve([]);
                return result;
            }
            var fields = _.find(this.models, function (model) {
                return model.model === 'pos.order';
            }).fields;
            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 7500 * orders.length;

            // Keep the order ids that are about to be sent to the
            // backend. In between create_from_ui and the success callback
            // new orders may have been added to it.
            var order_ids_to_sync = _.pluck(orders, 'id');

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var args = [_.map(orders, function (order) {
                order.to_invoice = options.to_invoice || false;
                return order;
            })];
            return rpc.query({
                model: 'pos.order',
                method: 'create_from_ui',
                args: args,
                kwargs: {context: session.user_context},
            }, {
                timeout: timeout,
                shadow: !options.to_invoice
            })
                .then(function (server_ids) {
                    _.each(order_ids_to_sync, function (order_id) {
                        self.db.remove_order(order_id);
                    });
                    self.set('failed', false);
                    if (server_ids.length != 0) {
                        for (var item in server_ids) {
                            rpc.query({
                                model: 'pos.order',
                                method: 'search_read',
                                args: [[['id', '=', server_ids[item]]], fields],
                                limit: 1,
                            })
                                .then(function (order) {
                                    self.orders.unshift(order[0]);
                                });
                        }
                    }
                    self.load_server_data();
                    return server_ids;
                }).catch(function (type, error) {
                    if (error.code === 200) {    // Business Logic Error, not a connection problem
                        //if warning do not need to display traceback!!
                        if (error.data.exception_type == 'warning') {
                            delete error.data.debug;
                        }

                        // Hide error if already shown before ...
                        if ((!self.get('failed') || options.show_error) && !options.to_invoice) {
                            self.gui.show_popup('error-traceback', {
                                'title': error.data.message,
                                'body': error.data.debug
                            });
                        }
                        self.set('failed', error);
                    }
                    console.error('Failed to send orders:', orders);
                });
        },

    });

});