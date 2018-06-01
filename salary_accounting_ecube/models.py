# -*- coding: utf-8 -*-
from openerp import models, fields, api

class EmployeeExtend(models.Model):
	_inherit = 'hr.employee'

	partner_id = fields.Many2one('res.partner',string="Related Partner")



	@api.model
	def create(self, vals):
		new_record = super(EmployeeExtend, self).create(vals)
		
		Receivable_list=[]
		Payable_list=[]
		account_receivable=self.env['account.account'].search([('user_type_id.name','=','Receivable')])
		for x in account_receivable:
			Receivable_list.append(x)
		account_payable=self.env['account.account'].search([('user_type_id.name','=','Payable')])
		for y in account_payable:
			Payable_list.append(y)
		member_entries = self.env['res.partner']
		customer_id = member_entries.create({
				'name': new_record.name,
				'property_account_receivable_id': Receivable_list[0],
				'property_account_payable_id': 	Payable_list[0],
				'employee': True,
				'customer': False,
			})

		new_record.partner_id =customer_id.id


		return new_record



class PartnerExtend(models.Model):
	_inherit = 'res.partner'

	employee = fields.Boolean(string="Employee")



	





