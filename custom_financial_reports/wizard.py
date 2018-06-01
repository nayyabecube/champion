# #-*- coding:utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as published by
# #    the Free Software Foundation, either version 3 of the License, or
# #    (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
from odoo import models, fields, api


class GenerateBalanceSheet(models.Model):
	_name = "ecube.balance.sheet"

	form = fields.Date("From")
	to = fields.Date("To")
	state = fields.Selection([
		('balance_sheet', 'Balance Sheet'),
		('profit_loss', 'Profit and Loss'),
		('cash', 'Cash Flow'),
		], string='Status', copy=False, index=True, track_visibility='onchange')
	name = fields.Many2one('ecube.report.structure',string='Name of Report')

class AccountMoveExtension(models.Model):
	_inherit = "account.move"

	branch = fields.Many2one("res.partner",string="Branch")