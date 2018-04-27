# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning, ValidationError


class account_bank_extension(models.Model):
	_inherit = 'account.bank.statement'


	account_id = fields.Many2one('account.account', string = "Account Head")
	payment_jurnl = fields.Many2one('account.journal', string = "Payment Journal")
	state = fields.Selection([('open', 'New'), ('in_progress', 'In Progress'),('confirm', 'Validated')], string='Status', required=True, readonly=True, copy=False, default='open')
	current_balance = fields.Float(string = "Current Balance", compute = "compute_balance")

	@api.onchange('account_id')
	def compute_name(self):
		if self.account_id:
			self.name = str(self.account_id.code) + " - " + str(self.account_id.name) + " - " + str(self.date)

	@api.one
	def compute_balance(self):
		debit = 0
		credit = 0
		entries = self.env['account.move.line'].search([('account_id','=',self.account_id.id)])

		for amounts in entries:
			debit = debit + amounts.debit
			credit = credit + amounts.credit
	
		self.current_balance = debit - credit


	@api.multi
	def in_progress(self):
		self.state = "in_progress"

	@api.multi
	def validate_entries(self):
		self.post()
		self.state = "confirm"
		for x in self.line_ids:
			x.journal_entry_id.post()
			
	@api.multi
	def reset_progress(self):
		self.state = "in_progress"
		for lines in self.line_ids:
			lines.journal_entry_id.button_cancel()


	@api.multi
	def post(self):
		value = 0
		journal_entries = self.env['account.move']
		journal_entries_lines = self.env['account.move.line']
		for x in self.line_ids:
			x.journal_entry_id.unlink()
			if not x.journal_entry_id:
				if x.paid > 0 and self.payment_jurnl:
					value = self.payment_jurnl.id
				else:
					value = self.journal_id.id
				create_journal = journal_entries.create({
					'journal_id': value,
					'date':x.date,
					'ref' : self.name,
					})
				if x.amount > 0:
					debit_account = self.account_id.id
					credit_account = x.account_id.id
				if x.amount < 0:
					debit_account = x.account_id.id
					credit_account = self.account_id.id 
				debit = journal_entries_lines.create({
					'account_id':debit_account,
					'partner_id':x.partner_id.id,
					'name':x.name,
					'debit':abs(x.amount),
					'credit':0,
					'move_id':create_journal.id,
					})

				credit = journal_entries_lines.create({
					'account_id':credit_account,
					'partner_id':x.partner_id.id,
					'name':x.name,
					'debit':0,
					'credit':abs(x.amount),
					'move_id':create_journal.id,
					})

				x.journal_entry_id = create_journal.id






class account_bank_extension_line(models.Model):
	_inherit = 'account.bank.statement.line'


	
	journal_entry_id = fields.Many2one('account.move',string="Debit")
	bank = fields.Many2one('account.account',string="Credit")
	paid = fields.Float(string="Paid")
	received = fields.Float(string="Received")

	@api.onchange('paid')
	def getamount(self):
		if self.paid:
			self.received = 0
			self.amount = self.paid * -1

	@api.onchange('received')
	def getamountrec(self):
		if self.received:
			self.paid = 0
			self.amount = self.received 


	@api.multi
	def unlink(self):
		self.journal_entry_id.unlink()
		super(account_bank_extension_line, self).unlink()


	


class account_move_extend(models.Model):
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


class account_act_extension(models.Model):
	_inherit = 'account.account'


	bank = fields.Boolean()


	


