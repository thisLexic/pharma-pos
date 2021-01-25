from datetime import date

from odoo import models, fields, api


class Product_Name(models.Model):
    _name = 'pharma_pos.product_name'
    _description = 'Contains names of products'
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Cannot have duplicate product names!')
    ]

    name = fields.Char(string="Product Name")
    date_added = fields.Date(string="Date Added", default=date.today())
