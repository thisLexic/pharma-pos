from odoo import models, fields, api

class Batch(models.Model):
    _name = 'pharma_pos.batch'
    _description = 'Contains a batch of packs with the same prices'

    price_id = fields.Many2one('pharma_pos.price', string="Product")