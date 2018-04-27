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
###################################################
from openerp import models, fields, api
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta
import time
import re

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.production_data_statement.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('production_data_statement.customer_report')
        active_wizard = self.env['production.data'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['production.data'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['production.data'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to


        invoices = self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice'),('invoice_id.date_invoice','>=',record_wizard.date_from),('invoice_id.date_invoice','<=',record_wizard.date_to),('invoice_id.state','=','draft')])

        records = self.env['daily.production.tree'].search([('date','>=',record_wizard.date_from),('date','<=',record_wizard.date_to)])

        open_records = self.env['daily.production.tree'].search([('date','<',record_wizard.date_from)])

        open_invoices = self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice'),('invoice_id.date_invoice','<',record_wizard.date_from),('invoice_id.state','=','draft')])


        def get_kg():
            value = 0
            for x in records:
                if x.uom == "Kg":
                    value = value + x.qty_lit

            return value

        def get_mt():
            value = 0
            for x in records:
                value = value + x.qty_kg

            return value

        def get_lit():
            value = 0
            for x in records:
                if x.uom == "Ltr":
                    value = value + x.qty_lit

            return value

        def tot_lit():
            value = 0
            for x in records:
                value = value + x.qty_lit

            return value
            

        def inv_kg():
            value = 0
            new = 0
            for x in invoices:
                if x.product_id.attribute_value_ids:
                    for y in x.product_id.attribute_value_ids:
                        if y.attribute_id.name == "Size" or y.attribute_id.name == "size":
                            if re.findall(r"[-+]?\d*\.\d+|\d+", y.name):
                                n = float(re.findall("[-+]?\d*\.\d+|\d+", y.name)[0])
                                qty_l = n * x.quantity
                                if x.product_id.product_receipe:
                                    qty_k = qty_l * float(x.product_id.product_receipe.wpl)
                                    new = new + qty_k
            value = new

            return value

        def inv_lit():
            value = 0
            for x in invoices:
                if x.product_id.attribute_value_ids:
                    for y in x.product_id.attribute_value_ids:
                        if y.attribute_id.name == "Size" or y.attribute_id.name == "size":
                            if re.findall(r"[-+]?\d*\.\d+|\d+", y.name):
                                n = float(re.findall("[-+]?\d*\.\d+|\d+", y.name)[0])
                                new = n * x.quantity
                                value = value + new

            return value

        def inv_sub():
            value = 0
            for x in invoices:
                value = value + x.price_subtotal

            return value

        def get_open_lit():
            daily = 0
            inv = 0
            value = 0
            for x in open_records:
                daily = daily + x.qty_lit
            for y in open_invoices:
                if y.product_id.attribute_value_ids:
                    for z in y.product_id.attribute_value_ids:
                        if z.attribute_id.name == "Size" or z.attribute_id.name == "size":
                            if re.findall(r"[-+]?\d*\.\d+|\d+", z.name):
                                n = float(re.findall("[-+]?\d*\.\d+|\d+", z.name)[0])
                                new = n * y.quantity
                                inv = inv + new

            value = daily - inv

            return value

        def get_open_kg():
            daily = 0
            inv = 0
            value = 0
            for x in open_records:
                daily = daily + x.qty_kg
            for y in open_invoices:
                if y.product_id.attribute_value_ids:
                    for z in y.product_id.attribute_value_ids:
                        if z.attribute_id.name == "Size" or z.attribute_id.name == "size":
                            if re.findall(r"[-+]?\d*\.\d+|\d+", z.name):
                                n = float(re.findall("[-+]?\d*\.\d+|\d+", z.name)[0])
                                new = n * y.quantity
                                if y.product_id.product_receipe:
                                    qty_k = new * float(y.product_id.product_receipe.wpl)
                                    inv = inv + qty_k
            
            value = daily - inv

            return value


        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'date':date,
            'tot_lit':tot_lit,
            'get_lit':get_lit,
            'get_kg':get_kg,
            'get_mt':get_mt,
            'inv_kg':inv_kg,
            'inv_lit':inv_lit,
            'inv_sub':inv_sub,
            'get_open_lit':get_open_lit,
            'get_open_kg':get_open_kg,
            'date_from':date_from,

            }

        return report_obj.render('production_data_statement.customer_report', docargs)