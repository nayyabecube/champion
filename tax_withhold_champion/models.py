from odoo import models, fields, api
import xlsxwriter
import webbrowser


class TaxWithold(models.Model):
	_name = 'tax.withold'
	_rec_name = 'ref_no'

	supplier       = fields.Many2one('res.partner',string="Supplier" )
	date           = fields.Date(string="Date")
	amount         = fields.Float(string="Amount")
	tax            = fields.Float(string="Tax Withheld")
	tax_name       = fields.Char(string="Tax Name")
	payment_sec    = fields.Char(string="Payment Section")
	ref_no     	   = fields.Char(string="Refrence No.")
	paid		   = fields.Boolean(string="Paid")
	challan_no     = fields.Char(string="Challan No.")
	state          = fields.Selection([
					('unpaid', 'Unpaid'),
					('paid', 'Paid'),
					], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='unpaid')



	@api.multi
	def epay(self):
		pass

class TaxWitholdWizard(models.Model):
	_name = "tax.withold.wizard"

	paid		   = fields.Boolean(string="Paid")
	challan_no     = fields.Char(string="Challan No.", required = True)

	@api.multi
	def punch(self):
		active_class = self.env['tax.withold'].browse(self._context.get('active_ids'))
		if active_class:
			print "Active"
			for x in active_class:
				x.challan_no = self.challan_no ; x.paid = self.paid

class epayWizard(models.Model):
	_name = "epay.wizard"

	challan_no     = fields.Char(string="Challan No.", required = True)

	@api.multi
	def get_epay(self):
		# active_class = self.env['tax.withold'].browse(self._context.get('active_id'))
		active_class 	= self.env['tax.withold'].search([('challan_no','=',self.challan_no)])

		if active_class:

			with xlsxwriter.Workbook("/home/odoo/Desktop/ePayment_xlsx_Report.xlsx") as workbook:
						
				main_heading = workbook.add_format({
					"bold": 1,
					"align": 'center',
					"valign": 'vcenter',
					"font_color":'black',
					"bg_color": '999999'
					})

				main_data = workbook.add_format({
					"align": 'center',
					"valign": 'vcenter'

					})

				worksheet = workbook.add_worksheet('Sheet1')

				worksheet.set_column('A:J', 20)

				worksheet.write('A1', 'Payment Section',main_heading)
				worksheet.write('B1', 'TaxPayer_NTN',main_heading)
				worksheet.write('C1', 'TaxPayer_CNIC',main_heading)
				worksheet.write('D1', 'TaxPayer_Name',main_heading)
				worksheet.write('E1', 'TaxPayer_City',main_heading)
				worksheet.write('F1', 'TaxPayer_Address',main_heading)
				worksheet.write('G1', 'TaxPayer_Status',main_heading)
				worksheet.write('H1', 'TaxPayer_Business_Name',main_heading)
				worksheet.write('I1', 'Taxable_Amount',main_heading)
				worksheet.write('J1', 'Tax_Amount',main_heading)

				row = 1
				col = 0

				for x in active_class:
					if self.challan_no == x.challan_no:
						z 	= self.env['customer.payment.bcube'].search([('number','=',x.ref_no)])
						worksheet.write_string (row, col,str(1),main_data)
						worksheet.write_string (row, col+1,z.partner_id.cp_ntn,main_data)
						worksheet.write_string (row, col+2,z.partner_id.cp_cnic,main_data)
						worksheet.write_string (row, col+3,z.partner_id.name,main_data)
						worksheet.write_string (row, col+4,z.partner_id.city,main_data)
						worksheet.write_string (row, col+5,z.partner_id.street + z.partner_id.street2,main_data)
						worksheet.write_string (row, col+6,"INDIVIDUAL",main_data)
						worksheet.write_string (row, col+7,str(z.partner_id.function),main_data)
						worksheet.write_string (row, col+8,str(x.amount),main_data)
						worksheet.write_string (row, col+9,str(x.tax),main_data)
					row +=1



				in_row = 1
				in_col = 0

				worksheet = workbook.add_worksheet("PaymentSections")

				worksheet.set_column('A:A', 15)
				worksheet.set_column('B:B', 30)
				worksheet.set_column('C:C', 50)
				worksheet.set_column('D:D', 10)

				worksheet.write('A1', 'Section',main_heading)
				worksheet.write('B1', 'Tax Payment Nature',main_heading)
				worksheet.write('C1', 'Tax Payment Section',main_heading)
				worksheet.write('D1', 'Code',main_heading)


				worksheet.write_string (in_row, in_col,str(1),main_data)
				worksheet.write_string (in_row, in_col+1,str(1),main_data)
				worksheet.write_string (in_row, in_col+2,str(1),main_data)
				worksheet.write_string (in_row, in_col+3,str(1),main_data)


class ChallanWithold(models.Model):
	_name = 'challan.withold'
	_rec_name = 'challan_no'


	date_from  = fields.Date(string="Date From" ,required=True)
	date_to    = fields.Date(string="Date To" ,required=True)
	pay_date   = fields.Date(string="Payment Date")
	challan_no = fields.Char(string="Challan No.")
	challan_id = fields.One2many('challan.withold.tree','challan_tree')
	state      = fields.Selection([
					('draft', 'Draft'),
					('validate', 'Validate'),
					], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

	@api.multi
	def generate(self):
		if self.challan_id:
			self.challan_id.unlink()
		rec = self.env['tax.withold'].search([('state','=','unpaid'),('date','>=',self.date_from),('date','<=',self.date_to)])
		challan_tree = self.env['challan.withold.tree'].search([])
		for x in rec:
			create_challan_tree = challan_tree.create({
				'supplier' : x.supplier.id,
				'date': x.date,
				'tax_name': x.tax_name,
				'amount':x.amount,
				'tax': x.tax,
				'payment_sec': x.payment_sec,
				'withold': x.id,
				'challan_tree': self.id,
				})
			x.state = 'paid'

	@api.multi
	def generate_report(self):
		with xlsxwriter.Workbook("/home/odoo/odoo10/custom_addons/champion/customer_invoices.xlsx") as workbook:
			main_heading = workbook.add_format({
				"bold": 1,
				"align": 'center',
				"valign": 'vcenter',
				"font_color":'red',
				"bg_color": '#CCFFCC',
				"border": 1
				})

			main_data = workbook.add_format({
				"align": 'center',
				"valign": 'vcenter'

				})

			worksheet = workbook.add_worksheet('Summary')

			worksheet.set_column('A:J', 20)

			worksheet.write('A1', 'Payment Section',main_heading)
			worksheet.write('B1', 'Tax Payer NTN',main_heading)
			worksheet.write('C1', 'Tax Payer CNIC',main_heading)
			worksheet.write('D1', 'Tax Payer Name',main_heading)
			worksheet.write('E1', 'Tax Payer City',main_heading)
			worksheet.write('F1', 'Tax Payer Address',main_heading)
			worksheet.write('G1', 'Tax Payer Status',main_heading)
			worksheet.write('H1', 'Tax Payer Business',main_heading)
			worksheet.write('I1', 'Taxable Amount',main_heading)
			worksheet.write('J1', 'Tax Amount',main_heading)

			row = 1
			col = 0
			
			for x in self.challan_id:
				if x.payment_sec:
					worksheet.write_string (row, col,x.payment_sec,main_data)
				if x.supplier.cp_ntn:
					worksheet.write_string (row, col+1,x.supplier.cp_ntn,main_data)
				if x.supplier.cp_cnic:
					worksheet.write_string (row, col+2,x.supplier.cp_cnic,main_data)
				if x.supplier:
					worksheet.write_string (row, col+3,x.supplier.name,main_data)
				if x.supplier.city:
					worksheet.write_string (row, col+4,x.supplier.city,main_data)
				if x.supplier.street:
					worksheet.write_string (row, col+5,x.supplier.street,main_data)
				worksheet.write_string (row, col+6,' ',main_data)
				worksheet.write_string (row, col+7,' ',main_data)
				worksheet.write_string (row, col+8,str(x.amount),main_data)
				worksheet.write_string (row, col+9,str(x.tax),main_data)
				row += 1

		url = "/home/odoo/odoo10/custom_addons/champion/customer_invoices.xlsx"
		webbrowser.open(url)

				

class ChallanWitholdTree(models.Model):
	_name = 'challan.withold.tree'

	supplier       = fields.Many2one('res.partner',string="Supplier")
	date           = fields.Date(string="Date")
	amount         = fields.Float(string="Amount")
	tax            = fields.Float(string="Tax Amount")
	tax_name       = fields.Char(string="Tax Name")
	payment_sec    = fields.Char(string="Payment Section")
	challan_tree   = fields.Many2one('challan.withold')
	withold        = fields.Many2one('tax.withold')

	@api.multi
	def unlink(self):
		for x in self:
			if x.withold:
				x.withold.state='unpaid'
		super(ChallanWitholdTree, self).unlink()

		return True
