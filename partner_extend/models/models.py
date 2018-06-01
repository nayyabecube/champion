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
		""" FUnction set all res.partner records set recevable adn payable adn button is hide in xml """
		Receivable_list=[]
		account_receivable=self.env['account.account'].search([('user_type_id.name','=','Receivable')])
		for x in account_receivable:
			if "Receivable" in x.name:
				Receivable_list.append(x.id)


		payable_list_id = []
		account_payable=self.env['account.account'].search([('user_type_id.name','=','Payable')])
		for y in account_payable:
			if "Payable" in y.name:
				payable_list_id.append(y.id)

		customer = self.env['res.partner'].search([])
		for z in customer:
			z.property_account_receivable_id = Receivable_list[0]
			z.property_account_payable_id = payable_list_id[0]



	@api.model
	def create(self, vals):
		new_record = super(partner_champion, self).create(vals)
		Receivable_list=[]
		account_receivable=self.env['account.account'].search([('user_type_id.name','=','Receivable')])
		for x in account_receivable:
			if "Receivable" in x.name:
				Receivable_list.append(x.id)
		new_record.property_account_receivable_id = Receivable_list[0]

		payable_list_id = []
		account_payable=self.env['account.account'].search([('user_type_id.name','=','Payable')])
		for y in account_payable:
			if "Payable" in y.name:
				payable_list_id.append(y.id)
		new_record.property_account_payable_id = payable_list_id[0]
		return new_record

class tax_champion(models.Model):
	_inherit = 'account.tax'


	payment_sec = fields.Char(string="Payment Section")


class fiscal_champion(models.Model):
	_inherit = 'account.fiscal.position'

	nonfiler = fields.Boolean(string="Non Filer")