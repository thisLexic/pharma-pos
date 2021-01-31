from datetime import date

from odoo import models, fields, api


class Product_Name(models.Model):
    _name = 'pharma_pos.product_name'
    _description = 'Contains names of products'
    _rec_name ='string_rep'
    _sql_constraints = [
        ('product_name_generic_name_branded_name_unique', 'unique(string_rep)', 'This product name already exists!')
    ]

    @api.depends('generic_name', 'branded_name')
    def _get_string_rep(self):
        for record in self:
            try:
                record.string_rep = record.branded_name + " ({})".format(record.generic_name)
            except:
                pass

    generic_name = fields.Char(string="Generic Name")
    branded_name = fields.Char(string="Branded Name")
    date_added = fields.Date(string="Date Added", default=date.today())
    string_rep = fields.Char(string="Med", compute="_get_string_rep", store=True)


class Product_Size(models.Model):
    _name = 'pharma_pos.product_size'
    _description = 'Contains sizes of products'
    _rec_name ='string_rep'
    _sql_constraints = [
        ('product_size_size_unique', 'unique(size)', 'This product size already exists!')
    ]

    @api.depends('size', 'product_type_id')
    def _get_string_rep(self):
        for record in self:
            try:
                record.string_rep = record.size + " {}".format(getStringRepresentation(record.product_type_id.name_get()))
            except:
                pass

    size = fields.Char(string="Product Size")
    date_added = fields.Date(string="Date Added", default=date.today())
    product_type_id = fields.Many2one('pharma_pos.product_type', string="Type")
    string_rep = fields.Char(string="Size", compute="_get_string_rep", store=True)
    
class Product_Type(models.Model):
    _name = 'pharma_pos.product_type'
    _description = 'Contains types of products'
    _rec_name ='consumption_method'
    _sql_constraints = [
        ('product_type_consumption_method_unique', 'unique(consumption_method)', 'This product type already exists!')
    ]

    consumption_method = fields.Char(string="Type")

class Product(models.Model):
    _name = 'pharma_pos.product'
    _description = 'The product that is sold with its name (Product_Name) and unit (Product_Size) specified using foreign keys'
    _rec_name ='string_rep'
    _sql_constraints = [
        ('product_store_code_unique', 'unique(store_code)', 'This store code already exists!'),
        ('product_supplier_code_unique', 'unique(supplier_code)', 'This supplier code already exists!'),
        ('product_product_name_id_product_size_id_unique', 'unique(string_rep)', 'This combination of product name and size already exists!')
    ]

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

class Pack(models.Model):
    _name = 'pharma_pos.pack'
    _description = 'The pack of a product which may contain one or more products within one pack'
    _sql_constraints = [
        ('pack_bar_code', 'unique(bar_code)', 'This bar code already exists!'),
        ('pack_product_id_count', 'unique(count, product_id)', 'A product with that number of items per pack already exists!')
    ]

    product_id = fields.Many2one('pharma_pos.product', string="Item")
    count = fields.Integer(string="Item/s per Pack")
    bar_code = fields.Char(string="Bar Code")
    is_sold = fields.Boolean(string="Is Sold", default=True)

# Helper Functions

def getStringRepresentation(nonString):
    return nonString[0][1]