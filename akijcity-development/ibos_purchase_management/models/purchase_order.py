from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    payment_status = fields.Selection([
        ('no', 'Nothing to Payment'),
        ('paid', 'Fully Paid'),
        ('to_payment', 'Waiting Payments')
    ], default='no', string="Payment Status")