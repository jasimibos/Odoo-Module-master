odoo.define('ibos_pos_partial_payment.pos_partial_payment', function (require) {
    "use strict";

    var PosBaseWidget = require('point_of_sale.BaseWidget');
    var gui = require('point_of_sale.gui');
    var models = require('point_of_sale.models');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var utils = require('web.utils');
    var screens = require("point_of_sale.screens");
    var _t = core._t;

    screens.PaymentScreenWidget.include({
        events: {
            'click .partial-payment': '_pos_credit_payment',
        },
        template: 'PaymentScreenWidget',

        _pos_credit_payment: function () {
            self = this;
            var order = this.pos.get_order();
            var total = order.get_total_with_tax();
            var total_paid = order.get_total_paid() - order.get_change()

            var customer_id = this.emp_id
            customer_id.push(total)
            customer_id.push(total_paid)

            var emp = rpc.query({
                model: 'hr.employee',
                method: 'search_employee_rec',
                args: [customer_id],
            }).then(function (result) {
                if(result === 1){
                    self.finalize_validation();
                }
                else{
                    self.gui.show_popup('alert',{
                                'title': _t("Warning"),
                                'body': _t('Customer credit limit gets out of bound.'),
                                });
                }

            }).catch(function (error) {
                console.log("NO DATA",error);
            });
            var rmv1 = customer_id.pop() // removing 1st last element from the list array
            var rmv2 = customer_id.pop() // removing 2nd last element from the list array
        },
    });

});