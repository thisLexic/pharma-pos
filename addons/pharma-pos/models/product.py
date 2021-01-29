from datetime import date

from odoo import models, fields, api


class Product_Name(models.Model):
    _name = 'pharma_pos.product_name'
    _description = 'Contains names of products'
    _sql_constraints = [
        ('product_name_generic_name_branded_name_unique', 'unique(generic_name, branded_name)', 'This product name already exists!')
    ]

    def name_get(self):
        result = []
        for record in self:
            name = record.generic_name + " ({})".format(record.branded_name)
            result.append((record.id, name))
        return result

    generic_name = fields.Char(string="Generic Name")
    branded_name = fields.Char(string="Branded Name")
    date_added = fields.Date(string="Date Added", default=date.today())


class Product_Size(models.Model):
    _name = 'pharma_pos.product_size'
    _description = 'Contains sizes of products'
    _sql_constraints = [
        ('product_size_size_unique', 'unique(size)', 'This product size already exists!')
    ]

    def name_get(self):
        result = []
        for record in self:
            name = record.size + " {}".format(record.consumption_method)
            result.append((record.id, name))
        return result

    size = fields.Char(string="Product Size")
    date_added = fields.Date(string="Date Added", default=date.today())
    consumption_method = fields.Selection([('tablet', 'Tablet'), ('injectable', 'Injectable'), ('capsule', 'Capsule'), ('syrup', 'Syrup')], string="Type")
    

class Product(models.Model):
    _name = 'pharma_pos.product'
    _description = 'The product that is sold with its name (Product_Name) and unit (Product_Size) specified using foreign keys'

    product_name_id = fields.Many2one('pharma_pos.product_name', string="Med")
    product_size_id = fields.Many2one('pharma_pos.product_size', string="Size")