# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ChampionAccountInvLine(models.Model):
    _inherit = 'account.invoice.line'

    discounted_amount = fields.Float(string="Discounted Amount",
        store=True, readonly=True, compute='_compute_discounted_amount')
    cp_tax_amount = fields.Monetary(string='Tax Amount',
        store=True, readonly=True, compute='_compute_amount_tax_line')


    @api.one
    @api.depends('discounted_amount', 'invoice_line_tax_ids')
    def _compute_amount_tax_line(self):
    	if self.discounted_amount and self.invoice_line_tax_ids:
    		for line in self.invoice_line_tax_ids:
    			self.cp_tax_amount = self.cp_tax_amount + ((self.discounted_amount * line.amount)/ 100)



    @api.one
    @api.depends('discount', 'price_subtotal')
    def _compute_discounted_amount(self):
        if self.discount:
            self.discounted_amount = self.price_subtotal