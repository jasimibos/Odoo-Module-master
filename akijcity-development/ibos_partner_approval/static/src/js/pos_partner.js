odoo.define('ibos_partner_approval.pos_partner', function (require){
    "use strict"

    var core = require("web.core");
    var screens = require("point_of_sale.screens");
    var _t = core._t;

    screens.ClientListScreenWidget.include({
        init: function(parent, options) {
            this._super(parent, options);
        },
        show: function() {
            var self = this;
            this._super();

            if(this.pos.config.allow_create_partner == false){
                this.$(".new-customer").addClass("oe_hidden");
            }
        },
    })
})