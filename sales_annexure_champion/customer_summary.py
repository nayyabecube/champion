#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import xlsxwriter
import webbrowser
import os
import errno
import urllib
from openerp import models, fields, api
from datetime import datetime, timedelta

class RegionWiseReport(models.AbstractModel):
	_name = 'report.sales_annexure_champion.report_module'



	@api.model
	def render_html(self,docids, data=None):
		report_obj = self.env['report']
		report = report_obj._get_report_from_name('sales_annexure_champion.report_module')
		active_wizard = self.env['sales.annexure'].search([])
		emp_list = []
		for x in active_wizard:
			emp_list.append(x.id)
		emp_list = emp_list
		emp_list_max = max(emp_list) 

		record_wizard = self.env['sales.annexure'].search([('id','=',emp_list_max)])

		record_wizard_del = self.env['sales.annexure'].search([('id','!=',emp_list_max)])
		record_wizard_del.unlink()

		records = self.env['account.invoice'].search([('date_invoice','>=',record_wizard.form),('date_invoice','<=',record_wizard.to),('type','=','out_invoice')])
		print records
		print "kkkkkkkkkkkkkkkkkkkkkkkkk"


			
		self.sales_annexure(records)


		docargs = {
			'doc_ids': docids,
			'doc_model': 'account.invoice',
			'docs': records,
			'data': data,
			}

		return report_obj.render('sales_annexure_champion.report_module', docargs)

	def sales_annexure(self,records):
		def getTypes():
			value = " "
			for rec in records:
				for tax in rec.tax_line_ids:
					if "Sales" in tax.name:
						taxes = self.env["account.tax"].search([('name','=',tax.name)])
						if taxes.cp_sales_type.name:
							value = taxes.cp_sales_type.name
							return value
							print "-------------------------------------------------------"
						else:
							return " " 


		def getDesc():
			value = " "
			for rec in records:
				for tax in rec.tax_line_ids:
					if "Sales" in tax.name:
						taxes = self.env["account.tax"].search([('name','=',tax.name)])
						if taxes.cp_item_desc.name:
							value = taxes.cp_item_desc.name
							return value
							print "-------------------------------------------------------"
						else:
							return " "


		def getRate():
			value = 0
			for rec in records:
				for tax in rec.tax_line_ids:
					if "Sales" in tax.name:
						taxes = self.env["account.tax"].search([('name','=',tax.name)])
						if taxes.amount:
							value = str(taxes.amount)
							return value
							print "-------------------------------------------------------"
						else:
							return " "


		# def getAmt():
		# 	print "gggggggggggggggggggggggggggggggggggggggggggggggggggggggggg"
		# 	value = 0
		# 	for rec in records:
		# 		if rec.state == "paid":
		# 			for tax in rec.tax_line_ids:
		# 				if "Sales" in tax.name:
		# 					print tax.name
		# 					print "dddddddddddddddddddddddddddddddddddddddddddddddddd"
		# 					if tax.amount:
		# 						print tax.amount
		# 						print "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
		# 						value = str(tax.amount)
		# 						return value
		# 					else:
		# 						return " "



		# def extraAmt():
		# 	print "////////////////////////////////////////////////////////////"
		# 	value = 0
		# 	for rec in records:
		# 		if rec.state == "paid":
		# 			for tax in rec.tax_line_ids:
		# 				if "Extra" in tax.name:
		# 					print tax.name
		# 					print "????????????????????????????????????????????????????"
		# 					if tax.amount:
		# 						print tax.amount
		# 						print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		# 						value = str(tax.amount)
		# 						return value
		# 					else:
		# 						return " "


		# further = []
		# for rec in records:
		# 	if rec.state == "paid":
		# 		for tax in rec.tax_line_ids:
		# 			if "Further" in tax.name:
		# 				further.append(tax)

							# print tax.name
							# print "????????????????????????????????????????????????????"
							# if tax.amount:
							# 	print tax.amount
							# 	print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
							# 	value = str(tax.amount)
							# 	return value
							# else:
							# 	return " "




		# def furtherAmt(records):
		# 	print records
		# 	print records.tax_line_ids
		# 	# value = 0
		# 	# for rec in records:
		# 	if records.state == "paid":
		# 		print "*******************************************"	
		# 		for tax in records.tax_line_ids:
		# 			if "Further" in tax.name:
		# 				print tax.name
		# 				print "................................................................"
		# 				if tax.amount:
		# 					print tax.amount
		# 					print "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
		# 					value = str(tax.amount)
		# 					return value
		# 				else:
		# 					return " "
		# 			else:
		# 				continue

		
		print "cccccccccccccccccccccccccccccccccccccccccccccccc"
		print getTypes()
		print "cccccccccccccccccccccccccccccccccccccccccccccccc"
		row = 1
		col = 0
		# filename = "/static/src/customer_invoices.xlxs"
		# if not os.path.exists(os.path.dirname(filename)):
		# 	try:
		# 		os.makedirs(os.path.dirname(filename))
		# 	except OSError as exc:
		# 		if exc.errno != errno.EEXIST:
		# 			raise
		# dir_path = os.path.dirname(os.path.realpath(__file__))

		workbook = xlsxwriter.Workbook("/home/odoo10/odoo-dev/projects/champion_original/sales_annexure_champion/static/src/customer_invoices.xlsx")
		worksheet = workbook.add_worksheet()

		main_heading = workbook.add_format({
			"bold": 1,
			"align": 'center',
			"valign": 'vcenter'
			})

		main_data = workbook.add_format({
			"align": 'center',
			"valign": 'vcenter'
			})


		worksheet.set_column('A:A', 5)
		worksheet.set_column('B:E', 20)
		worksheet.set_column('F:F', 40)
		worksheet.set_column('G:J', 20)
		worksheet.set_column('K:K', 30)
		worksheet.set_column('L:L', 15)
		worksheet.set_column('M:M', 45)
		worksheet.set_column('N:O', 15)
		worksheet.set_column('P:P', 40)
		worksheet.set_column('Q:Q', 25)
		worksheet.set_column('R:R', 15)
		worksheet.set_column('S:T', 25)
		worksheet.set_column('U:V', 15)
		worksheet.set_column('W:W', 20)
		worksheet.write('A1', 'Sr',main_heading)
		worksheet.write('B1', 'Buyer NTN',main_heading)
		worksheet.write('C1', 'Buyer CNIC',main_heading)
		worksheet.write('D1', 'Buyer Name',main_heading)
		worksheet.write('E1', 'Buyer Type',main_heading)
		worksheet.write('F1', 'Sale Origination Province of Supplier',main_heading)
		worksheet.write('G1', 'Document Type',main_heading)
		worksheet.write('H1', 'Document Number',main_heading)
		worksheet.write('I1', 'Document Date',main_heading)
		worksheet.write('J1', 'HS Code',main_heading)
		worksheet.write('K1', 'Sale Type',main_heading)
		worksheet.write('L1', 'Rate',main_heading)
		worksheet.write('M1', 'Description',main_heading)
		worksheet.write('N1', 'Quantity',main_heading)
		worksheet.write('O1', 'UOM',main_heading)
		worksheet.write('P1', 'Value of Sales Excluding Sales Tax',main_heading)
		worksheet.write('Q1', 'Sales Tax/ FED in ST Mode',main_heading)
		worksheet.write('R1', 'Extra Tax',main_heading)
		worksheet.write('S1', 'ST Withheld at Source',main_heading)
		worksheet.write('T1', 'SRO No. / Schedule No.',main_heading)
		worksheet.write('U1', 'Item Sr. No..',main_heading)
		worksheet.write('V1', 'Further Tax.',main_heading)
		worksheet.write('W1', 'Total Value of Sales.',main_heading)

		count = 1
		for line in records:
			amount = 0
			extra = 0
			furt = 0
			if line.state == "draft":
				for x in line.tax_line_ids:
					if "Sales" in x.name:
						amount = x.amount
					if "Extra" in x.name:
						extra = x.amount
					if "Further" in x.name:
						furt = x.amount
				worksheet.write_string (row, col,str(count),main_data)
				if line.partner_id.cp_ntn:
					worksheet.write_string (row, col+1,line.partner_id.cp_ntn,main_data)
				if line.partner_id.cp_cnic:
					worksheet.write_string (row, col+2,str(line.partner_id.cp_cnic),main_data)
				worksheet.write_string (row, col+3,line.partner_id.name,main_data)
				if line.partner_id.buyer_type:
					worksheet.write_string (row, col+4,line.partner_id.buyer_type,main_data)
				worksheet.write_string (row, col+5,'Punjab',main_data)
				worksheet.write_string (row, col+6,'SI',main_data)
				if line.number:
					worksheet.write_string (row, col+7,line.number,main_data)
				worksheet.write_string (row, col+8,datetime.strptime(line.date_invoice, '%Y-%m-%d').strftime('%d/%m/%Y'),main_data)
				# worksheet.write_string (row, col+9)
				worksheet.write_string (row, col+10,getTypes(),main_data)
				worksheet.write_string (row, col+11,getRate(),main_data)
				worksheet.write_string (row, col+12,getDesc(),main_data)
				# worksheet.write_string (row, col+13,main_data)
				# worksheet.write_string (row, col+14,main_data)
				worksheet.write_string (row, col+15,str(line.amount_untaxed),main_data)
				worksheet.write_string (row, col+16,str(amount),main_data)
				worksheet.write_string (row, col+17,str(extra),main_data)
				# worksheet.write_string (row, col+18)
				# worksheet.write_string (row, col+19)
				# worksheet.write_string (row, col+20)
				worksheet.write_string (row, col+21,str(furt),main_data)
				# worksheet.write_string (row, col+22)
				count += 1
				row += 1
		workbook.close()



		# dls = "file:///home/nayyab/customer_invoices.xlsx"
		# urllib.urlretrieve(dls, "%s/static/src/customer_invoices.xlxs" % dir_path[:-8])
		# if  not "%s/static/src/customer_invoices.xlxs" % dir_path[:-8]:
		#     os.system("mv  customer_invoices.xlxs %s/static/src/customer_invoices.xlxs" % dir_path[:-8])

		url = "/home/odoo10/odoo-dev/projects/champion_original/sales_annexure_champion/static/src/customer_invoices.xlsx"
		# print "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
		webbrowser.open(url)
		# print "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
		# # # created_file = urllib.URLopener()
		# # # created_file.retrieve(url, 'CustomerInvoice.xlsx')
		# urllib.urlretrieve(url, 'CustomerInvoice.xlsx')
		# # # wget.download(url)
		# # print "xxxxxxxxxxxxxxxxxxxxxxxx"



# set path of file at 306 and 204 line
# set path of file at 306 and 204 line