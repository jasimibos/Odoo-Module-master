/*
    License: OPL-1
    author: farooq@aarsol.com   
*/
odoo.define('ibos_pos_invoce_receipt.model', function (require) {
    var models = require('point_of_sale.models');    
    var core = require('web.core');    
    var _t = core._t;    
    var session = require('web.session');
    var rpc = require('web.rpc');

    var _super_PosModel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        get_model: function (_name) {
            var _index = this.models.map(function (e) {
                return e.model;
            }).indexOf(_name);
            if (_index > -1) {
                return this.models[_index];
            }
            return false;
        },
        initialize: function (session, attributes) {
            var self = this;            
            var company_model = this.get_model('res.company');
            company_model.fields.push('street','city');            
            
            _super_PosModel.initialize.apply(this, arguments);          

        },        
        get_config: function () {
            return this.config;
        },        
      
    });

});
