from odoo import models, fields, api

class Batch(models.Model):
    _name = 'pharma_pos.batch'
    _description = 'Contains a batch of packs with the same prices'

    price_id = fields.Many2one('pharma_pos.price', string="Product", domain="[('is_sold', '=', True)]")
    batch_number = fields.Char(string="Batch Number")
    bought_count = fields.Integer(string="Packs Bought")
    sold_count = fields.Integer(string="Packs Sold")
    left_count = fields.Integer(string="Packs Left")
    expiration_date = fields.Date(string="Expiration Date")