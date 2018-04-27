# -*- coding: utf-8 -*-

from odoo import models, fields, api

class partner_champion(models.Model):
	_inherit = 'res.partner'

	tax_payment = fields.Many2many('account.tax',string="Tax on Payments")
	buyer_type  = fields.Selection([
		('Registered','Registered'),
		('Unregistered','Unregistered')
		],string="Buyer Type")
   # filer_type   = fields.Selection([('filer', 'Filer'),('nonfiler', 'Non Filer')],string="Type")
	filer_type = fields.Selection([('filer', 'Filer'), ('nonfiler', 'Non Filer')], string="Type", default='filer')

	@api.multi
	def create_invoice(self):
		Receivable_list=[]
		account_receivable=self.env['account.account'].search([('user_type_id.name','=','Receivable')])
		for x in account_receivable:
			if "Receivable" in x.name:
				Receivable_list.append(x)

		customer = self.env['res.partner'].search([])
		for x in customer:
			x.property_account_receivable_id = Receivable_list[0].id



	@api.model
	def create(self, vals):
		new_record = super(DiscountAmount, self).create(vals)
		Receivable_list=[]
		account_receivable=self.env['account.account'].search([('user_type_id.name','=','Receivable')])
		for x in account_receivable:
			if "Receivable" in x.name:
				Receivable_list.append(x)
		
		new_record.property_account_receivable_id = Receivable_list[0].id

		return new_record

class tax_champion(models.Model):
	_inherit = 'account.tax'


	payment_sec = fields.Char(string="Payment Section")


class fiscal_champion(models.Model):
	_inherit = 'account.fiscal.position'

	nonfiler = fields.Boolean(string="Non Filer")