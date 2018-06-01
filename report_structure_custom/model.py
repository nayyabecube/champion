# -*- coding: utf-8 -*- 
from odoo import models, fields, api
from odoo.exceptions import UserError
class ecube_report_structure(models.Model):
    _name = 'ecube.report.structure'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    description = fields.Selection([
        ('balance_sheet', 'Balance Sheet'),
        ('profit_loss', 'Profit and Loss'),
        ('cash', 'Cash Flow'),
        ], string='Description')
    report_link = fields.One2many('ecube.report.structure.details','report_tree')
    division_link = fields.One2many('ecube.report.structure.divisions','divisions_tree')
    division = fields.Many2many('res.users',string='Division')

    # @api.model
    # def create(self,vals):
    #     new_record = super(ecube_report_structure, self).create(vals)

    #     records = self.env['ecube.report.structure'].search([('name','=',new_record.name),('description','=',new_record.description)])
    #     if records:
    #         raise UserError('You Cannot Create' + " " + str(new_record.description) + " " +'with same Name')

class ecube_report_structure_details(models.Model):
    _name = 'ecube.report.structure.details'
    _order='sequence'
    _defaults={'sequence':2}

    description = fields.Many2one('description.class',string="Description")
    account_head = fields.Many2many('account.account',string="Account Head")
    summary2 = fields.Char(string="Summary Heads")
    sequence = fields.Integer(string='sequence',default=10)
    level = fields.Integer(string="Level")
    entry_type = fields.Selection([
                        ('heading', 'Heading'),
                        ('account', 'Account'),
                        ('total', 'Total'),
                        ('grand_total', 'Grand Total'),
                        ('other_report', 'Other Report')
                        ], string='Type')
    nature = fields.Selection([
                        ('debit', 'Debit'),
                        ('credit', 'Credit'),
                        ], string='Nature', default='debit')
    report_tree = fields.Many2one('ecube.report.structure')
    amount = fields.Float(string="Amount")

    @api.model 
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('dem.seq')
        new_record = super(ecube_report_structure_details, self).create(vals) 
        return new_record

class ecube_report_structure_divisions(models.Model):
    _inherit = 'ecube.report.structure.details'
    _name = 'ecube.report.structure.divisions'

    partner = fields.Char(string="Partner")
    report_id = fields.Char(string="Report IDs")

    divisions_tree = fields.Many2one('ecube.report.structure')


class descriptionClass(models.Model):
    _name = 'description.class'

    name = fields.Char(string="Description")