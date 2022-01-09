# -*- coding: utf-8 -*-from odoo import api, fields, models
from odoo import api, fields, models, _


class ImageSlider(models.Model):
    _name = "image.slider"
    _description = "Ecommerce Image Slider"

    name = fields.Char(string='Title', required=True, tracking=True)
    image = fields.Image(string="Upload Your Image")
    active = fields.Boolean('Active', default=True)
