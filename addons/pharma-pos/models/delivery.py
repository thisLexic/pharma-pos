from odoo import models, fields, api
from odoo.exceptions import ValidationError

from .tools import getStringRepresentation

class Batch(models.Model):
    _name = 'pharma_pos.batch'
    _description = 'Contains a batch of packs with the same prices'
    _rec_name ='string_rep'
    _sql_constraints = [
        ('price_id_delivery_id_expiration_date_batch_number_unique', 'unique(price_id, delivery_id, expiration_date, batch_number)', 'This product already has an entry for this delivery. Please use that one instead of making a new one')
    ]

    @api.depends('price_id.string_rep', 'expiration_date', 'batch_number')
    def _get_string_rep(self):
        for record in self:
            if record.price_id and record.expiration_date:
                record.string_rep = getStringRepresentation(record.price_id) + " ({} | ".format(record.expiration_date) + "{})".format(record.batch_number)
            else:
                record.string_rep = "No Value"

    price_id = fields.Many2one('pharma_pos.price', string="Product", domain="[('is_sold', '=', True)]")
    delivery_id = fields.Many2one('pharma_pos.delivery', string="Delivery")
    batch_number = fields.Char(string="Batch Number")
    bought_count = fields.Integer(string="Packs Bought")
    sold_count = fields.Integer(string="Packs Sold")
    left_count = fields.Integer(string="Packs Left")
    unboxed_count = fields.Integer(string="Packs Unboxed")
    expiration_date = fields.Date(string="Expiration Date")
    string_rep = fields.Char(string="Name", compute="_get_string_rep", store=True)

    def unbox(self):   
        pack_count = self.price_id.pack_id.count
        if pack_count <= 1:
            raise ValidationError('You can only unbox packs with more than one item in them! This only has one item. Try another item!')

        self.unboxed_count = self.unboxed_count + 1

        price_ids = self.env['pharma_pos.price'].search([
            ('pack_id.product_id', '=', self.price_id.pack_id.product_id.id),
            ('is_sold', '=', True),
            ('pack_id.count', '=', 1)
        ])
        if len(price_ids) > 1:
            raise ValidationError('Cannot be unboxed because of duplicate price entries')
        elif len(price_ids) == 0:
            raise ValidationError('Cannot be unboxed because of a missing price entry with a count of 1 that matches this product')
        else:
            price = price_ids[0].id

        price_id = price
        batch_number = self.batch_number
        bought_count = pack_count
        sold_count = 0
        left_count = pack_count
        unboxed_count = 0
        expiration_date = self.expiration_date

        batch_obj = self.env['pharma_pos.batch'].create({
            'price_id': price_id,
            'batch_number': batch_number,
            'bought_count': bought_count,
            'sold_count': sold_count,
            'left_count': left_count,
            'unboxed_count': unboxed_count,
            'expiration_date': expiration_date,
        })

class Delivery(models.Model):
    _name = 'pharma_pos.delivery'
    _description = 'Contains one or many batches which go from one company to another company'
    _rec_name ='invoice_date'
    _sql_constraints = [
        ('invoice_date_unique', 'unique(invoice_date)', 'Only one delivery can be made per day. Please add the batches to the delivery instead')
    ]

    batch_ids = fields.One2many('pharma_pos.batch', 'delivery_id', string='Batches')
    to_company_id = fields.Many2one('res.company', string="To")
    from_company_id = fields.Many2one('res.company', string="From")
    code = fields.Char(string="Code")
    invoice_date = fields.Date(string="Invoice Date")