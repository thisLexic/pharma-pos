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
            name = record.branded_name + " ({})".format(record.generic_name)
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
            name = record.size + " {}".format(getStringRepresentation(record.product_type_id.name_get()))
            result.append((record.id, name))
        return result

    size = fields.Char(string="Product Size")
    date_added = fields.Date(string="Date Added", default=date.today())
    product_type_id = fields.Many2one('pharma_pos.product_type', string="Type")
    
class Product_Type(models.Model):
    _name = 'pharma_pos.product_type'
    _description = 'Contains types of products'
    _sql_constraints = [
        ('product_type_consumption_method_unique', 'unique(consumption_method)', 'This product type already exists!')
    ]

    def name_get(self):
        result = []
        for record in self:
            name = record.consumption_method
            result.append((record.id, name))
        return result

    consumption_method = fields.Char(string="Type")

class Product(models.Model):
    _name = 'pharma_pos.product'
    _description = 'The product that is sold with its name (Product_Name) and unit (Product_Size) specified using foreign keys'
    _sql_constraints = [
        ('product_store_code_unique', 'unique(store_code)', 'This store code already exists!'),
        ('product_supplier_code_unique', 'unique(supplier_code)', 'This supplier code already exists!'),
        ('product_product_name_id_product_size_id_unique', 'unique(product_name_id, product_size_id)', 'This combination of product name and size already exists!')
    ]

    def name_get(self):
        result = []
        for record in self:
            name = record.string_rep
            result.append((record.id, name))
        return result

    @api.depends('product_name_id', 'product_size_id')
    def _get_string_rep(self):
        for record in self:
            try:
                record.string_rep = getStringRepresentation(record.product_name_id.name_get()) + " " + getStringRepresentation(record.product_size_id.name_get())
            except:
                pass

    product_name_id = fields.Many2one('pharma_pos.product_name', string="Med")
    product_size_id = fields.Many2one('pharma_pos.product_size', string="Size")
    store_code = fields.Char(string="Store Code")
    supplier_code = fields.Char(string="TGP Code")
    date_added = fields.Date(string="Date Added", default=date.today())
    is_sold = fields.Boolean(string="Is Sold", default=True)
    string_rep = fields.Char(string="Name", compute="_get_string_rep", store=True)


# Helper Functions

def getStringRepresentation(nonString):
    return nonString[0][1]