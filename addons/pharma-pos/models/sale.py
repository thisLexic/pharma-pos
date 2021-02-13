from odoo import models, fields, api

class Sale(models.Model):
    _name = 'pharma_pos.sale'
    _description = 'Sell products one at a time'

    def _default_currency_id(self):
        return self.env['res.currency'].search([('name', '=', 'PHP')], limit=1).id

    batch_id = fields.Many2one('pharma_pos.batch', string="Product")
    currency_id = fields.Many2one('res.currency', string="Currency", default=_default_currency_id)
    price = fields.Monetary(string="Price")
    price_total = fields.Monetary(string="Price Total")
    count = fields.Integer(string="Count", default=1)