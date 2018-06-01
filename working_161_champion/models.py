from odoo import models, fields, api
import xlsxwriter
from pprint import pprint
import json


class TaxWork(models.Model):
	_name = 'taxes.work'
	_rec_name = 'date_from'

	date_from       = fields.Date(string="Date From")
	date_to         = fields.Date(string="Date To")
	sum_id     = fields.One2many('tax.tree','tax_id')
	
	@api.multi
	def generate_suppliers(self):
		all_suppliers 	= self.env['res.partner'].search([('supplier','=',True)])
		journal_ent 	= self.env['account.move'].search([])
		line 			= self.env['tax.tree'].search([])
		credit_amount = 0 
		debit_amount = 0
		total_payment = 0
		p_credit_amount = 0 
		p_debit_amount  = 0
		sum_id = []
		delete = []
		delete = delete.append(2)
		self.sum_id = delete

		if self.date_from and self.date_to:
			for x in all_suppliers:
				credit_amount = 0 
				debit_amount  = 0
				total_payment = 0
				ven_payment = 0
				w_tax = 0
				w_tax_pay = 0
				vendor_pay 	= self.env['account.invoice'].search([('type','=',"in_invoice"),('partner_id','=',x.id)])
				tax_w = self.env['tax.withold'].search([('supplier','=',x.name)])
				for y in journal_ent:
					for z in y.line_ids:
						if x.name == z.partner_id.name and z.account_id.user_type_id.type == "payable":
							if z.date <= self.date_from:
								if z.debit > 0:
									debit_amount = debit_amount + z.debit
								elif z.credit > 0:
									credit_amount = credit_amount +z.credit

				for ven in vendor_pay:
					if ven.date_invoice >= self.date_from and self.date_to >= ven.date_invoice:
						ven_payment = ven_payment + ven.amount_total 

				for tw in tax_w:
					if tw.date >= self.date_from and self.date_to >= tw.date:
						w_tax = w_tax + tw.tax
						if tw.paid== True:
							w_tax_pay = w_tax_pay +tw.tax

				if credit_amount > 0 or debit_amount > 0 or total_payment >-1:	
					customer_payments = self.env['customer.payment.bcube'].search([('partner_id','=',x.id)])
					for a in customer_payments:
						if a.date >= self.date_from and self.date_to >= a.date:
							total_payment = total_payment + a.amount
				create_line = line.create({
					'suppliers' : x.name,
					'open_bal' : credit_amount - debit_amount,
					'purchases' : ven_payment,
					'payment' : total_payment,
					'tax_appl' : w_tax,
					'tax_dedt' : w_tax,
					'tax_paid' : w_tax_pay,
					'close_bal' : (credit_amount - debit_amount) + ven_payment - total_payment,
					'tax_id' : self.id,
					})
		
	@api.multi
	def xl_report(self):
		with xlsxwriter.Workbook("/home/odoo/Desktop/161_Working_Xlsx_Report.xlsx") as workbook:
			main_heading = workbook.add_format({
				"bold": 1,
				"align": 'center',
				"valign": 'vcenter',
				"font_color":'red',
				"bg_color": '#CCFFCC'
				})

			main_data = workbook.add_format({
				"align": 'center',
				"valign": 'vcenter'

				})

			worksheet = workbook.add_worksheet('Summary')

			worksheet.set_column('A:H', 20)

			worksheet.write('C1', 'Date From',main_heading)
			worksheet.write('E1', 'Date To',main_heading)
			worksheet.write_string (1, 2,self.date_from,main_data)
			worksheet.write_string (1, 4,self.date_to,main_data)

			worksheet.write('A4', 'Supplier',main_heading)
			worksheet.write('B4', 'Opening Balance',main_heading)
			worksheet.write('C4', 'purchases',main_heading)
			worksheet.write('D4', 'Payments',main_heading)
			worksheet.write('E4', 'Tax Applicable',main_heading)
			worksheet.write('F4', 'Tax Deducted',main_heading)
			worksheet.write('G4', 'Tax Paid',main_heading)
			worksheet.write('H4', 'Closing Balance',main_heading)
			row = 4
			col = 0

			for x in self.sum_id:
				worksheet.write_string (row, col,x.suppliers,main_data)
				worksheet.write_string (row, col+1,x.open_bal,main_data)
				worksheet.write_string (row, col+2,x.purchases,main_data)
				worksheet.write_string (row, col+3,x.payment,main_data)
				worksheet.write_string (row, col+4,x.tax_appl,main_data)
				worksheet.write_string (row, col+5,x.tax_dedt,main_data)
				worksheet.write_string (row, col+6,x.tax_paid,main_data)
				worksheet.write_string (row, col+7,x.close_bal,main_data)
				row += 1
				

			all_suppliers 	= self.env['res.partner'].search([('supplier','=',True)])
			journal_ent 	= self.env['account.move'].search([])
			line 			= self.env['tax.tree'].search([])
			for x in self.sum_id:
				
				worksheet = workbook.add_worksheet(x.suppliers)
				in_row = 1
				in_col = 0
				worksheet.set_column('A:H', 20)
				worksheet.write('B1', 'Company:',main_heading)
				worksheet.write('C1', 'Date To:',main_heading)
				worksheet.write('D1', 'Date From:',main_heading)
				worksheet.write('E1', 'Target Moves:',main_heading)
				worksheet.write('A4', 'Date',main_heading)
				# worksheet.write('B4', 'Account',main_heading)
				worksheet.write('B4', 'Ref',main_heading)
				worksheet.write('C4', 'Debit',main_heading)
				worksheet.write('D4', 'Credit',main_heading)
				worksheet.write('E4', 'Balance',main_heading)
				if self.date_from and self.date_to:
					worksheet.write_string (in_row, in_col+1,str(x.suppliers),main_data)
					worksheet.write_string (in_row, in_col+2,self.date_from,main_data)
					worksheet.write_string (in_row, in_col+3,self.date_to,main_data)
					worksheet.write_string (in_row, in_col+4,"All Entries",main_data)
					credit_amount = 0 
					debit_amount  = 0
					total_payment = 0
					bal = float(x.open_bal)
					for y in journal_ent:
						if self.date_from <= y.date and self.date_to >= y.date:
							for z in y.line_ids:
								credit_amount = 0 
								debit_amount  = 0
								if z.partner_id.name == x.suppliers and z.account_id.user_type_id.type == "payable":
									if z.debit > 0:
										bal = bal - z.debit
										debit_amount = z.debit
									elif z.credit > 0:
										bal = bal + z.credit
										credit_amount = z.credit

									
									worksheet.write_string (in_row+3, in_col,str(z.date),main_data)
									# worksheet.write_string (in_row+3, in_col+1,str(z.account_id.user_type_id.type),main_data)
									worksheet.write_string (in_row+3, in_col+1,str(y.name),main_data)
									worksheet.write_string (in_row+3, in_col+2,str(debit_amount),main_data)
									worksheet.write_string (in_row+3, in_col+3,str(credit_amount),main_data)
									worksheet.write_string (in_row+3, in_col+4,str(bal),main_data)
									in_row += 1
	# @api.multi
	# def run_q(self):
	# 	self._cr.execute("""\
	# 			SELECT      move_id
	# 			FROM        account_move_line
	# 			WHERE       move_id in %s
	# 			GROUP BY    move_id
	# 			HAVING      abs(sum(debit) - sum(credit)) > %s
	# 			""", (tuple(self.ids), 10 ** (-max(5, prec))))


	# 	cr = self.env.cr
	# 	self.env.cr.execute("SELECT amount_total,partner_id FROM  account_invoice AS a WHERE a.date_invoice >= %s AND a.date_invoice <= %s",(self.date_from,self.date_to))
	# 	self.env.cr.execute("SELECT price_subtotal,amount_total, a.partner_id FROM  account_invoice AS a ,account_invoice_line As b WHERE a.id = b.invoice_id" )
	# 	print "--------------------------------------------"
	# 	print self.env.cr.fetchall()
	# 	pprint (self.env.cr.dictfetchall())
	# 	ddict = self.env.cr.dictfetchall()
	# 	print type(self.env.cr.dictfetchall())
	# 	d= {}
	# 	d = ddict[0:]
	# 	print json.dumps(ddict, indent=2)
	# 	print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	# 	print json.dumps(d, indent=2)
	# 	print d[1]['amount_total']
	# 	add =0
	# 	count = 0
	# 	for x in d:
	# 		add = add + d[count]['amount_total']
	# 		a = self.env['res.partner'].search([('id','=',d[count]['partner_id'])])
	# 		print a.name
	# 		count += 1



	# 	print add
	# 	print "--------------------------------------------"
	# 	pass
		

class TaxTree(models.Model):
	_name = "tax.tree"

	suppliers  = fields.Char(string="Supplier")
	open_bal   = fields.Char(string="Opening Balance")
	purchases  = fields.Char(string="Purchases")
	payment    = fields.Char(string="Payment")
	tax_appl   = fields.Char(string="Tax Applicable")
	tax_dedt   = fields.Char(string="Tax Deducted")
	tax_paid   = fields.Char(string="Tax Paid")
	close_bal  = fields.Char(string="Closing Balance")
	tax_id     = fields.Many2one('taxes.work')


