from odoo import models, fields, api

class Sale(models.Model):
    _name = 'pharma_pos.sale'
    _description = 'Sell products one at a time'
    _rec_name = 'price_total'

    def _default_currency_id(self):
        return self.env['res.currency'].search([('name', '=', 'PHP')], limit=1).id

    @api.depends('batch_id')
    def _get_price(self):
        for record in self:
            if record.batch_id:
                record.price = record.batch_id.price_id.price
            else:
                record.price = 0.0

    @api.depends('price', 'count')
    def _get_price_total(self):
        for record in self:
            if record.price and record.count:
                record.price_total = record.price * record.count
            else:
                record.price_total = 0.0

    pos_id = fields.Many2one('pharma_pos.pos', string="Pos")
    batch_id = fields.Many2one('pharma_pos.batch', string="Product", domain="[('left_count', '!=', 0)]")
    currency_id = fields.Many2one('res.currency', string="Currency", default=_default_currency_id)
    price = fields.Monetary(string="Price", compute="_get_price", store=True)
    price_total = fields.Monetary(string="Price Total", compute="_get_price_total", store=True)
    count = fields.Integer(string="Count", default=1)

class Pos(models.Model):
    _name = 'pharma_pos.pos'
    _description = 'Sell products by bulk'
    _rec_name = 'price_total'

    def _default_currency_id(self):
        return self.env['res.currency'].search([('name', '=', 'PHP')], limit=1).id

    @api.depends('sale_ids.price_total', 'is_senior')
    def _get_price_total(self):
        for record in self:
            if record.sale_ids:
                sale_total = 0
                for sale in record.sale_ids:
                    sale_total += sale.price_total
                if record.is_senior:
                    sale_total = sale_total * 0.8 
                record.price_total = sale_total
            else:
                record.price_total = 0.0

    sale_ids = fields.One2many('pharma_pos.sale', 'pos_id', string='Sales')
    currency_id = fields.Many2one('res.currency', string="Currency", default=_default_currency_id)
    datetime = fields.Datetime(string="Time", default=fields.Datetime.now())
    is_senior = fields.Boolean(string="Senior?", default=False)
    price_total = fields.Monetary(string="Sub Total", compute="_get_price_total", store=True)