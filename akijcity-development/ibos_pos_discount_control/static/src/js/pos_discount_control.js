odoo.define('ibos_pos_stock.discount_control', function (require){
    "use strict";
    var core = require("web.core");
    var screens = require("point_of_sale.screens");
    var _t = core._t;

    screens.NumpadWidget.include({
        init: function(parent) {
            this._super(parent);
        },
        applyAccessRights: function() {
            this._super();
            var has_discount_control_rights = !this.pos.config.restrict_discount_control;
            console.log("has_discount_control_rights:", has_discount_control_rights)
            this.$el.find('.mode-button[data-mode="discount"]')
                .toggleClass('disabled-mode', !has_discount_control_rights)
                .prop('disabled', !has_discount_control_rights);
            if (!has_discount_control_rights && this.state.get('mode')=='discount'){
                this.state.changeMode('quantity');
            }
        }
    })

})