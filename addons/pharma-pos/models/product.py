from datetime import date

from odoo import models, fields, api


class Product_Name(models.Model):
    _name = 'pharma_pos.product_name'
    _description = 'Contains names of products'
    _sql_constraints = [
        ('product_name_name_unique', 'unique(name)', 'This product name already exists!')
    ]

    name = fields.Char(string="Product Name")
    date_added = fields.Date(string="Date Added", default=date.today())


class Product_Size(models.Model):
    _name = 'pharma_pos.product_size'
    _description = 'Contains sizes of products'
    _sql_constraints = [
        ('product_size_size_unique', 'unique(size)', 'This product size already exists!')
    ]

    size = fields.Char(string="Product Size")
    date_added = fields.Date(string="Date Added", default=date.today())