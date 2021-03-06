from datetime import date

from odoo import models, fields, api
from odoo.exceptions import ValidationError

from .tools import getStringRepresentation


class Product_Name(models.Model):
    _name = 'pharma_pos.product_name'
    _description = 'Contains names of products'
    _rec_name ='string_rep'
    _sql_constraints = [
        ('product_name_generic_name_branded_name_unique', 'unique(generic_name, branded_name)', 'This product name already exists!')
    ]

    @api.depends('generic_name', 'branded_name')
    def _get_string_rep(self):
        for record in self:
            if record.generic_name and record.branded_name:
                record.string_rep = record.branded_name + " ({})".format(record.generic_name)
            elif record.generic_name:
                record.string_rep = "({})".format(record.generic_name)
            elif record.branded_name:
                record.string_rep = record.branded_name
            else:
                record.string_rep = "No Value"
                    
    generic_name = fields.Char(string="Generic Name")
    branded_name = fields.Char(string="Branded Name")
    date_added = fields.Date(string="Date Added", default=date.today())
    string_rep = fields.Char(string="Name", compute="_get_string_rep", store=True)


class Product_Size(models.Model):
    _name = 'pharma_pos.product_size'
    _description = 'Contains sizes of products'
    _rec_name ='string_rep'
    _sql_constraints = [
        ('product_size_size_unique', 'unique(size, product_type_id)', 'This product size already exists!')
    ]

    @api.depends('size', 'product_type_id.consumption_method')
    def _get_string_rep(self):
        for record in self:
            if record.size and record.product_type_id:
                record.string_rep = record.size + " {}".format(getStringRepresentation(record.product_type_id))
            else:
                record.string_rep = "No Value"

    size = fields.Char(string="Size")
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
        ('product_product_name_id_product_size_id_unique', 'unique(product_name_id, product_size_id)', 'This combination of product name and size already exists!')
    ]

    @api.depends('product_name_id.string_rep', 'product_size_id.string_rep')
    def _get_string_rep(self):
        for record in self:
            if record.product_name_id and record.product_size_id:
                record.string_rep = getStringRepresentation(record.product_name_id) + " " + getStringRepresentation(record.product_size_id)
            else:
                record.string_rep = "No Value"

    product_name_id = fields.Many2one('pharma_pos.product_name', string="Name")
    product_size_id = fields.Many2one('pharma_pos.product_size', string="Size")
    store_code = fields.Char(string="Store Code")
    supplier_code = fields.Char(string="TGP Code")
    date_added = fields.Date(string="Date Added", default=date.today())
    is_sold = fields.Boolean(string="Is Sold", default=True)
    string_rep = fields.Char(string="Name", compute="_get_string_rep", store=True)

class Pack(models.Model):
    _name = 'pharma_pos.pack'
    _description = 'The pack of a product which may contain one or more products within one pack'
    _rec_name ='string_rep'
    _sql_constraints = [
        ('pack_bar_code', 'unique(bar_code)', 'This bar code already exists!'),
        ('pack_product_id_count', 'unique(count, product_id)', 'A pack with that number of products per pack already exists!')
    ]

    @api.depends('product_id.string_rep', 'count')
    def _get_string_rep(self):
        for record in self:
            if record.product_id and record.count:
                record.string_rep = getStringRepresentation(record.product_id) + " {}x".format(record.count)
            else:
                record.string_rep = "No Value"

    product_id = fields.Many2one('pharma_pos.product', string="Product")
    count = fields.Integer(string="Products per Pack", default=1)
    bar_code = fields.Char(string="Bar Code")
    is_sold = fields.Boolean(string="Is Sold", default=True)
    string_rep = fields.Char(string="Name", compute="_get_string_rep", store=True)

class Price(models.Model):
    _name = 'pharma_pos.price'
    _description = 'The price of a pack record'
    _rec_name ='string_rep'
    _constraints = [
        ('_check_pack_id_is_sold', 'Only one active price can be assigned to a pack', ['pack_id', 'is_sold']),
     ]

    @api.depends('pack_id.string_rep', 'price')
    def _get_string_rep(self):
        for record in self:
            if record.pack_id and record.price:
                record.string_rep = getStringRepresentation(record.pack_id) + ": ₱{}".format(record.price)
            else:
                record.string_rep = "No Value"

    @api.constrains('pack_id.string_rep', 'is_sold')
    def _check_pack_id_is_sold(self):
        for record in self:
            if record.is_sold:
                # existing_active_prices = self.env['pharma_pos.price'].search([('pack_id', '=', record.pack_id.id), ('is_sold', '=', True)])
                price_ids = self.env['pharma_pos.price'].search([('pack_id', '=', record.pack_id.id), ('is_sold', '=', True)])
                if len(price_ids) > 1:
                    raise ValidationError('Only one active price can be assigned to a pack')


    def _default_currency_id(self):
         return self.env['res.currency'].search([('name', '=', 'PHP')], limit=1).id

    pack_id = fields.Many2one('pharma_pos.pack', string="Pack")
    price = fields.Monetary(string="Price")
    cost = fields.Monetary(string="Cost")
    currency_id = fields.Many2one('res.currency', string="Currency", default=_default_currency_id)
    date_added = fields.Date(string="Date Added", default=date.today())
    string_rep = fields.Char(string="Name", compute="_get_string_rep", store=True)
    is_sold = fields.Boolean(string="Is Sold", default=True)

