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
from openerp import models, fields, api
import xlsxwriter

class RegionWiseReport(models.AbstractModel):
    _name = 'report.champion_161_report.report_module'


    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('champion_161_report.report_module')
        active_wizard = self.env['champ.sales'].search([])

        records = self.env['account.invoice'].search([])
        self.summary_report(records)
        
       


        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'data': data
            }

        return report_obj.render('champion_161_report.report_module', docargs)


    def summary_report(self,records):
        for line in records:
            workbook = xlsxwriter.Workbook('summary_report_161.xlsx')
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

            worksheet.set_column('A:L', 20)
            worksheet.set_column('M:M', 30)
            worksheet.write('A1', 'Sr',main_heading)
            worksheet.write('B1', 'HEAD OF ACCOUNTS',main_heading)
            worksheet.write('C1', 'DATE OF PAYMENT',main_heading)
            worksheet.write('D1', 'EXPENSE CLAIMED',main_heading)
            worksheet.write('E1', 'PAYMENT MADE',main_heading)
            worksheet.write('F1', 'TAXABLE PAYMENT',main_heading)
            worksheet.write('G1', 'TAX DEDEUCTED',main_heading)
            worksheet.write('H1', 'TAX DEPOSITED',main_heading)
            worksheet.write('I1', 'BELOW TAXABLE',main_heading)
            worksheet.write('J1', 'EXEMPT PAYMENT',main_heading)
            worksheet.write('K1', 'NON TAXABLE',main_heading)
            worksheet.write('L1', 'PAYABLE EXPENSE',main_heading)
            worksheet.write('M1', 'REMARKS/ATTACHMENT',main_heading)
    
            row = 1
            col = 0
            for item in line.invoice_line_ids:
                worksheet.write_string (row, col,item.product_id.name,main_data)
                worksheet.write_string (row, col+1,item.product_id.name,main_data)
                worksheet.write_string (row, col+2,item.product_id.name,main_data)
                worksheet.write_string (row, col+3,item.product_id.name,main_data)
                worksheet.write_string (row, col+4,item.product_id.name,main_data)
                worksheet.write_string (row, col+5,item.product_id.name,main_data)
                worksheet.write_string (row, col+6,item.product_id.name,main_data)
                worksheet.write_string (row, col+7,item.product_id.name,main_data)
                worksheet.write_string (row, col+8,item.product_id.name,main_data)
                worksheet.write_string (row, col+9,item.product_id.name,main_data)
                worksheet.write_string (row, col+10,item.product_id.name,main_data)
                worksheet.write_string (row, col+11,item.product_id.name,main_data)
                worksheet.write_string (row, col+12,item.product_id.name,main_data)


            workbook.close()