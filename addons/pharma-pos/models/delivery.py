from odoo import models, fields, api

from .tools import getStringRepresentation

class Batch(models.Model):
    _name = 'pharma_pos.batch'
    _description = 'Contains a batch of packs with the same prices'
    _rec_name ='string_rep'

    @api.depends('price_id.string_rep', 'expiration_date')
    def _get_string_rep(self):
        for record in self:
            if record.price_id and record.expiration_date:
                record.string_rep = getStringRepresentation(record.price_id) + " ({})".format(record.expiration_date)
            else:
                record.string_rep = "No Value"

    price_id = fields.Many2one('pharma_pos.price', string="Product", domain="[('is_sold', '=', True)]")
    delivery_id = fields.Many2one('pharma_pos.delivery', string="Delivery")
    batch_number = fields.Char(string="Batch Number")
    bought_count = fields.Integer(string="Packs Bought")
    sold_count = fields.Integer(string="Packs Sold")
    left_count = fields.Integer(string="Packs Left")
    expiration_date = fields.Date(string="Expiration Date")
    string_rep = fields.Char(string="Name", compute="_get_string_rep", store=True)

class Delivery(models.Model):
    _name = 'pharma_pos.delivery'
    _description = 'Contains one or many batches which go from one company to another company'
    _rec_name ='invoice_date'

    batch_ids = fields.One2many('pharma_pos.batch', 'delivery_id', string='Batches')
    to_company_id = fields.Many2one('res.company', string="To")
    from_company_id = fields.Many2one('res.company', string="From")
    code = fields.Char(string="Code")
    invoice_date = fields.Date(string="Invoice Date")