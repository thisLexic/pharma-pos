from odoo import models, fields, api

class Sale(models.Model):
    _name = 'pharma_pos.sale'
    _description = 'Sell products one at a time'

    batch_id = fields.Many2one('pharma_pos.batch', string="Product")