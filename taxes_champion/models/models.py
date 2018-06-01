# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import Warning, ValidationError
import re

# import sys
# sys.setrecursionlimit(10000) 
class taxes_champion(models.Model):
	_inherit = 'account.tax'

	type_tax_use        = fields.Selection([
							('sale', 'Sales'),
							('purchase', 'Purchases'),
							('none', 'None'),
							('payment', 'Payment'),
							('receipt', 'Receipt'),
							('salary', 'Salary'),
							])
	amount_type         = fields.Selection([
							('group', 'Group of Taxes'),
							('fixed', 'Fixed'),
							('percent', 'Percentage of Price'),
							('division', 'Percentage of Price Tax Included')
							])
	cp_sales_type       = fields.Many2one('sales.type.bcube','Sales Type')
	cp_sro_no           = fields.Many2one('sro.schno.bcube','SRO No. /Schedule No')
	cp_item_sr_no       = fields.Many2one('item.srno.bcube','Item Sr. No')
	cp_item_desc        = fields.Many2one('item.desc.bcube','Description')
	fbr_tax_code        = fields.Char(string="FBR Tax Code")
	enable_child_tax    = fields.Boolean('Tax on Children')


class SalesTypeBcube(models.Model):
	_name               = 'sales.type.bcube'
	name                = fields.Char('Name')


class ItemSrnoBcube(models.Model):
	_name               = 'item.srno.bcube'
	name                = fields.Char('Name')


class SroSchnoBcube(models.Model):
	_name               = 'sro.schno.bcube'
	name                = fields.Char('Name')


class ItemDescBcube(models.Model):
	_name               = 'item.desc.bcube'
	name                = fields.Char('Name')


class AccountInvoiceBcube(models.Model):
	_inherit            = 'account.invoice'

	# date_invoice = fields.Date("date_invoice", required=True, readonly=False, select=True, default=lambda self: fields.date.today())
	vender_ntn = fields.Char(string="Vender NTN No.")
	sales_reg_no = fields.Char(string="Sales Tax Registeration No.")
	invoice_no = fields.Char(string="Invoice No.")
	payment_term = fields.Many2one('account.payment.term',string="Payment Term")
	discount_id = fields.Many2one('account.account',string="Discount Acoount")


	@api.multi
	def action_invoice_open(self):
		new_record = super(AccountInvoiceBcube, self).action_invoice_open()
		if self.move_id and self.type == "out_invoice":
			self.move_id.button_cancel()
			self.move_id.line_ids.unlink()
			new = 0
			for i in self.invoice_line_ids:
				new = new + ((i.quantity * i.price_unit) - i.price_subtotal)

			creat_dis = self.create_entry_lines(self.discount_id.id,self.partner_id.id,"Discount",new,0,self.move_id.id)
			creat_debit = self.create_entry_lines(self.partner_id.property_account_receivable_id.id,self.partner_id.id,self.partner_id.name,self.amount_total,0,self.move_id.id)
			for x in self.invoice_line_ids:
				value = 0
				value = x.quantity * x.price_unit
				creat_credit = self.create_entry_lines(x.account_id.id,self.partner_id.id,x.account_id.name,0,value,self.move_id.id)
			for z in self.tax_line_ids:
				creat_tax = self.create_entry_lines(z.account_id.id,self.partner_id.id,z.account_id.name,0,z.amount,self.move_id.id)


		return new_record


	def create_entry_lines(self,account,name,label,debit,credit,entry_id):
		self.env['account.move.line'].create({
				'account_id':account,
				'partner_id':name,
				'name':label,
				'debit':debit,
				'credit':credit,
				'move_id':entry_id,
				})

	@api.one
	def _compute_amount(self):
		res = super(AccountInvoiceBcube, self)._compute_amount()
		self.amount_tax = sum(line.amount for line in self.tax_line_ids)
		self.amount_total = self.amount_untaxed + self.amount_tax
		return res

	@api.onchange('partner_id')
	def _onchange_get_ntn(self):
		if self.type == "in_invoice":
			self.vender_ntn = self.partner_id.cp_ntn
			self.sales_reg_no = self.partner_id.cp_st_reg

	@api.onchange('date_invoice','payment_term')
	def due_Date(self):
		if self.type == "in_invoice":
			if self.payment_term and self.date_invoice:
				start_date = datetime.strptime(self.date_invoice,"%Y-%m-%d")
				if self.payment_term.name == "15 Days":
					self.date_due = start_date + timedelta(days=15)
				elif self.payment_term.name == "30 Days":
					self.date_due = start_date + timedelta(days=30)
				elif self.payment_term.name == "60 Net Days":
					self.date_due = start_date + timedelta(days=60)
				elif self.payment_term.name == "90 Days":
					self.date_due = start_date + timedelta(days=90)
				elif self.payment_term.name == "180 Days":
					self.date_due = start_date + timedelta(days=180)
				else:
					self.date_due = self.date_invoice


	@api.onchange('invoice_line_ids')
	def _onchange_invoice_line_ids(self):
		res = super(AccountInvoiceBcube, self)._onchange_invoice_line_ids()
		self.tax_line_ids = 0
		records = []
		taxes_ids = []
		for taxes in self.invoice_line_ids:
			for tax in taxes.bcube_taxes_id:
				if tax.id not in taxes_ids:
					taxes_ids.append(tax.id)
					
					records.append({
						'name':tax.name,
						'account_id':tax.account_id.id,
						'invoice_id':self.id,
						'tax_id':tax.id,
						'amount': 0,
						})
				
			self.tax_line_ids = records

		for taxes in self.invoice_line_ids:
			for tax in taxes.bcube_taxes_id:
				unit_price = taxes.price_unit -(taxes.price_unit * (taxes.discount/100) )
				amount_tax = self.invoice_line_ids.calculateTaxAmount(tax,taxes.quantity,unit_price)
				if self.tax_line_ids:
					for line in self.tax_line_ids:
						if line.name == tax.name:
							line.amount = line.amount + amount_tax
		return res


	@api.multi
	def reset(self):
		rec = self.env['account.move'].search([('ref','=',self.number)])
		if rec.state != 'posted' and self.move_id.state != 'posted':
			self.state = 'draft'
		else:
			raise  ValidationError('Cannot Send To Draft. First Unpost The Concerning Journal Enteries')

	@api.multi
	def taxes_set(self):
		Receivable_list=[]
		account_receivable=self.env['account.account'].search([('user_type_id.name','=','Receivable')])
		for x in account_receivable:
			if "Receivable" in x.name:
				Receivable_list.append(x.id)

		rec = self.env['account.invoice'].search([('type','=','out_invoice')])
		for line in rec:
			line.account_id=Receivable_list[0]

			if line.tax_line_ids:
				for x in line.tax_line_ids:
					records = self.env['account.tax'].search([])
					for y in records:
						if y.name == x.name:
							x.account_id = y.account_id.id
							if x.name== "Sales Tax":
								x.name = ""
								x.name = "Sales Tax 17 %"



	@api.multi
	def uom_set(self):
		rec =self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice')])
		for x in rec:
			x.uom = x.product_id.uom


	@api.multi
	def qty_set(self):
		rec =self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice')])
		for z in rec:
			if z.product_id:
				if z.product_id.attribute_value_ids:
					for x in z.product_id.attribute_value_ids:
						if x.attribute_id.name == "Size" or x.attribute_id.name == "size":
							if re.findall(r"[-+]?\d*\.\d+|\d+", x.name):
								n = float(re.findall("[-+]?\d*\.\d+|\d+", x.name)[0])
								if z.uom == 'Ltr':
									z.qty_lit = z.quantity * float(n)
									if z.product_id.product_receipe.wpl:
										z.qty_kg = z.qty_lit * float(z.product_id.product_receipe.wpl)
								if z.uom == 'Ml':
									n = n * 1000
									z.qty_lit = z.quantity * float(n)
									if z.product_id.product_receipe.wpl:
										z.qty_kg = z.qty_lit * float(z.product_id.product_receipe.wpl)
								if z.uom == 'Kg':
									z.qty_kg = z.quantity * float(n)
									if z.product_id.product_receipe.wpl:
										z.qty_lit = z.qty_kg / float(z.product_id.product_receipe.wpl)
								if z.uom == 'G':
									n = n * 1000
									z.qty_kg = z.quantity * float(n)
									if z.product_id.product_receipe.wpl:
										z.qty_lit = z.qty_kg / float(z.product_id.product_receipe.wpl)
								if z.uom == 'Mg':
									n = n * 1000000
									z.qty_kg = z.quantity * float(n)
									if z.product_id.product_receipe.wpl:
										z.qty_lit = z.qty_kg / float(z.product_id.product_receipe.wpl)





	@api.multi
	def taxes_setttttt(self):
		payable_list_id = []
		account_receivable=self.env['account.account'].search([('user_type_id.name','=','Payable')])
		for x in account_receivable:
			if "Payable" in x.name:
				payable_list_id.append(x.id)
		rec = self.env['account.invoice'].search([('type','=','in_invoice')])
		for line in rec:
			line.account_id=payable_list_id[0]
		# 	if line.tax_line_ids:
		# 		print " 111111111111111111111111111111111111" 
		# 		for x in line.tax_line_ids:
		# 			records = self.env['account.tax'].search([])
		# 			for y in records:
		# 				if y.name == x.name:
		# 					print "222222222222222222222222222222"
		# 					print y.name
		# 					print y.account_id.id
		# 					x.account_id = y.account_id.id
		# 					if x.name== "Sales Tax":
		# 						x.name = ""
		# 						x.name = "Sales Tax 17 %"








class AccountInvoiceLineBcube(models.Model):
	_inherit            = 'account.invoice.line'
	bcube_taxes_id      = fields.Many2many('account.tax',
		'account_invoice_line_tax', 'invoice_line_id', 'tax_id',
		string='Taxes', domain=[('type_tax_use','!=','none'), '|', ('active', '=', False), ('active', '=', True)], oldname='invoice_line_tax_id')
	bcube_amount_tax    = fields.Float(string = "Amount Tax")
	amount_incl_tax    = fields.Float(string = "Amount Inc. of Sales Tax")
	quantity = fields.Float(digits=(19,0))
	price_unit = fields.Float(digits=(19,4))
	check = fields.Boolean()


	@api.onchange('bcube_taxes_id','price_unit','quantity','discount')
	def onChBcubeTaxes(self):
		unit_price = self.price_unit -(self.price_unit * (self.discount/100) )
		self.bcube_amount_tax = self.calculateTaxAmount(self.bcube_taxes_id, self.quantity, unit_price)
		if self.invoice_id.type == "in_invoice":
			self.amount_incl_tax = self.price_subtotal + self.bcube_amount_tax


	@api.onchange('product_id')
	def getProductTaxes(self):
		all_taxes = []
		for x in self.invoice_id.partner_id.property_account_position_id.tax_ids:
			all_taxes.append((4,x.tax_dest_id.id))

		self.bcube_taxes_id = all_taxes
		self.discount = self.invoice_id.partner_id.discount
		

	def calculateTaxAmount(self, taxes, qty, price_unit):
		amount_tax = 0
		child_tax = 0
		child_tax_final=0
		for tax in taxes:
			if tax.enable_child_tax:
				if tax.children_tax_ids:
					child_tax = 0
					for childtax in tax.children_tax_ids:
						child_amount_tax = qty * price_unit * (childtax.amount/100) * (tax.amount/100)
		
						child_tax = child_tax + child_amount_tax 
					parent_tax = qty * price_unit * (tax.amount /100)
					child_tax_final = child_tax + parent_tax
					amount_tax += child_tax_final

			else:
				amount_tax += qty * price_unit * (tax.amount /100)
		
		return amount_tax

class DiscountAmount(models.Model):
	_inherit  = 'res.partner'
	discount = fields.Float(string="Discount%")

	



class ProductExtend(models.Model):
	_inherit  = 'product.template'

	naming_type =   fields.Selection([
					('general_store', 'General Store '),
					('finish_good', 'Finished Good'),
					('raw_material', 'Raw Material'),
					],string='Naming Type')
	product_receipe = fields.Many2one('product.receipe',string="Product Receipe")
	uom = fields.Selection([
		('Ltr', 'Ltr'),
		('Ml', 'Ml'),
		('Kg', 'Kg'),
		('G', 'G'),
		('Mg','Mg'),], string='Uom')

	product_pack = fields.Many2one('product.product',string="Pack Product")



	@api.model
	def create(self, vals):
		new_record = super(ProductExtend, self).create(vals)
		rec = self.env['product.product'].search([], order='id desc', limit=1)
		rec.naming_type = new_record.naming_type
		rec.product_receipe = new_record.product_receipe.id
		rec.uom = new_record.uom
		rec.product_pack = new_record.product_pack.id
		return new_record


	@api.multi
	def write(self, vals):
		res = super(ProductExtend, self).write(vals)
		rec = self.env['product.product'].search([('product_tmpl_id','=',self.id)])
		if rec:
			for x in rec:
				x.naming_type = self.naming_type
				x.product_receipe = self.product_receipe.id
				x.uom = self.uom
				x.product_pack = self.product_pack.id
		return res


class ProductExtended(models.Model):
	_inherit  = 'product.product'

	naming_type =   fields.Selection([
					('general_store', 'General Store '),
					('finish_good', 'Finished Good'),
					('raw_material', 'Raw Material'),
					],string='Naming Type')
	product_receipe = fields.Many2one('product.receipe',string="Product Receipe")
	uom = fields.Selection([
		('Ltr', 'Ltr'),
		('Ml', 'Ml'),
		('Kg', 'Kg'),
		('G', 'G'),
		('Mg','Mg'),], string='Uom')
	product_pack = fields.Many2one('product.product',string="Pack Product")

	@api.multi
	def get_type(self):
		rec = self.env['product.template'].search([('type','!=','product')])
		for x in rec:
			if x.type:
				x.type = "product"



class ProductReceipe(models.Model):
	_name  = 'product.receipe'


	name   = fields.Char('Category')
	wastage = fields.Integer('Wastage')
	wpl = fields.Float('WPL')
	receipe_id = fields.One2many('product.receipe.tree','receipe_tree')


class ProductReceipeTree(models.Model):
	_name  = 'product.receipe.tree'

	product = fields.Many2one('product.product',string="Product")
	ratio = fields.Float('Ratio')
	receipe_tree = fields.Many2one('product.receipe')


class move_extend_line(models.Model):
	_inherit = 'account.move'


	@api.multi
	def assert_balanced(self):
		if not self.ids:
			return True
		prec = self.env['decimal.precision'].precision_get('Account')

		self._cr.execute("""\
			SELECT      move_id
			FROM        account_move_line
			WHERE       move_id in %s
			GROUP BY    move_id
			HAVING      abs(sum(debit) - sum(credit)) > %s
			""", (tuple(self.ids), 10 ** (-max(5, prec))))
		# if len(self._cr.fetchall()) != 0:
		#     raise UserError(_("Cannot create unbalanced journal entry."))
		return True







# class product_variant_extension(models.Model):
# 	_inherit = 'product.product'

# 	new_record_name = fields.Char(string="Record Name") 
# 	test 			=  fields.Char(compute="_record_name")

# 	@api.onchange('attribute_value_ids','name')
# 	def _onchange_attribute_value_ids(self):
# 	    if self.name and self.attribute_value_ids:
# 	        self.new_record_name = self.name
# 	        for x in self.attribute_value_ids:
# 	            self.new_record_name = str(self.new_record_name)+" "+ str(x.name)

# 	@api.one
# 	def _record_name(self):
# 		print "xxXXXXXXXXXXX"
# 		print "xxXXXXXXXXXXX"
# 		print "xxXXXXXXXXXXX"
# 		self.test= self.new_record_name

# 	_rec_name = 'test'


	# @api.model
	# def create(self, vals): 
	# 	new_record = super(product_variant_extension, self).create(vals)
	# 	if new_record.name and new_record.attribute_value_ids:
	# 		new_record.new_record_name = new_record.name
	# 		for x in new_record.attribute_value_ids:
	# 			new_record.new_record_name = str(new_record.new_record_name)+" "+ str(x.name)
	# 	new_record._rec_name = new_record.new_record_name
	# 	return new_record
	# @api.multi
	# def name_get(self):
	# 	# TDE: this could be cleaned a bit I think

	# 	# def _name_get(d):
	# 	#     name = d.get('name', '')
	# 	#     code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
	# 	#     if code:
	# 	#         name = '[%s] %s' % (code,name)
	# 	#     return (d['id'], name)

	# 	partner_id = self._context.get('partner_id')
	# 	if partner_id:
	# 		partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
	# 	else:
	# 		partner_ids = []

	# 	# all user don't have access to seller and partner
	# 	# check access and use superuser
	# 	self.check_access_rights("read")
	# 	self.check_access_rule("read")

	# 	result = []
	# 	for product in self.sudo():
	# 		# display only the attributes with multiple possible values on the template
	# 		variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id')
	# 		variant = product.attribute_value_ids._variant_name(variable_attributes)

	# 		name = variant and "%s (%s)" % (product.name, variant) or product.name
	# 		sellers = []
	# 		if partner_ids:
	# 			sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and (x.product_id == product)]
	# 			if not sellers:
	# 				sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and not x.product_id]
	# 		if sellers:
	# 			for s in sellers:
	# 				seller_variant = s.product_name and (
	# 					variant and "%s (%s)" % (s.product_name, variant) or s.product_name
	# 					) or False
	# 				mydict = {
	# 						  'id': product.id,
	# 						  'name': seller_variant or name,
	# 						  'default_code': s.product_code or product.default_code,
	# 						  }
	# 				temp = _name_get(mydict)
	# 				if temp not in result:
	# 					result.append(temp)
	# 		else:
	# 			mydict = {
	# 					  'id': product.id,
	# 					  'name': name,
	# 					  'default_code': product.default_code,
	# 					  }
	# 			result.append(_name_get(mydict))
	# 	return result





#     @api.multi
#     def update_names(self):
#         all_products = self.env['product.product'].search([])
#         all_attributes = []
		# for x in all_products:
		#     all_attributes = []
		#     if x.name and x.attribute_value_ids:
		#         # name = x.name
		#         # req_name = name.split()
		#         x.name = str(x.name)+" "+ str(x.attribute_value_ids.name)
		#         # x.name = all_attributes
		#         print "xxxxxxxxxXXXXXX"
		#         print x.id       
		#         print x.name       
		#         print x.attribute_value_ids.name       

		# for x in all_products:
		#     all_attributes = []
		#     if x.name and x.attribute_value_ids:
		#         name = x.name
		#         req_name = name.split()
		#         for y in x.attribute_value_ids:
		#             all_attributes = str(req_name[0])+" "+ str(y.name)
		#             x.name = all_attributes



	# @api.model
	# def create(self, vals): 
	#     new_record = super(product_variant_extension, self).create(vals)
	#     all_attributes = ""
	#     for x in new_record.attribute_value_ids:
	#         all_attributes = str(all_attributes) + str(x.name)
	#     new_record.name = str(new_record.name)+ " " + all_attributes

	#     return new_record

	# @api.onchange('attribute_value_ids','name')
	# def _onchange_attribute_value_ids(self):
	#     all_attributes = []
	#     if self.name and self.attribute_value_ids:
	#         name = self.name
	#         req_name = name.split()
	#         for x in self.attribute_value_ids:
	#             all_attributes = str(req_name[0])+" "+ str(x.name)
	#             self.name = all_attributes       


	# @api.onchange('attribute_value_ids','name')
	# def _onchange_attribute_value_ids(self):
	#     all_attributes = []
	#     name = self.name
	#     req_name = name.split()
	#     for x in self.attribute_value_ids:
	#         all_attributes = str(req_name[0])+" "+ str(x.name)
	#         self.name = all_attributes       
	# @api.multi


	# def write(self, vals):
	#     all_attributes = []
	#     name = self.name
	#     req_name = name.split()
	#     for x in self.attribute_value_ids:
	#         all_attributes = str(req_name[0])+" "+ str(x.name)
	#     self.name = "all_attributes"
	#     result = super(product_variant_extension, self).write(vals)

	#     print "xxxxxxxxxxxxxxxxxxXXXXXXXXXXX"
	#     return result



