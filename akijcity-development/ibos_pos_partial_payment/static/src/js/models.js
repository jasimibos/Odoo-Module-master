odoo.define('ibos_pos_partial_payment.models', function (require) {
    "use strict";

    var models = require('point_of_sale.models')

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {
            var contact_model = _.find(this.models, function (model) {
                return model.model === 'res.partner';
            });
            contact_model.fields.push('employess_id');

            this.models.push({
                model: 'hr.employee',
                label: 'load_employee',
                fields: ['name', 'barcode', 'credit_limit', 'active'],
                loaded: function (self, emply) {
                    self.emply = emply;
                },
            });

            return _super_posmodel.initialize.call(this, session, attributes);
        },
    });
});