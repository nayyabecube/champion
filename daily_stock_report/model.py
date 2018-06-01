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
from datetime import date
from datetime import date, timedelta
import datetime
import re

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.daily_stock_report.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('daily_stock_report.customer_report')
        active_wizard = self.env['daily.stockreport'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['daily.stockreport'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['daily.stockreport'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        types = record_wizard.types



        d1 = datetime.datetime.strptime(record_wizard.date_from, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(record_wizard.date_to, "%Y-%m-%d")

        delta = d2 - d1
        dates = []
        for i in range(delta.days + 1):
            dates.append((d1 + timedelta(days=i)).strftime('%Y-%m-%d'))


        if types == "pack":


            records = []
            rec = self.env['product.product'].search([('categ_id.name','=','Packing Material')])
            for x in rec:
                records.append(x)


            def get_purchase(attr):
                value = 0
                rec = self.env['account.invoice.line'].search([('invoice_id.type','=','in_invoice'),('product_id.naming_type','=','finish_good'),('product_id.product_pack','=',attr),('invoice_id.date_invoice','<',date_from)])
                for x in rec:
                    value = value + x.quantity


                return value


            def get_purchase_val(attr,num):
                value = 0
                rec = self.env['account.invoice.line'].search([('invoice_id.type','=','in_invoice'),('product_id.naming_type','=','finish_good'),('product_id.product_pack','=',attr),('invoice_id.date_invoice','=',num)])
                for x in rec:
                    value = value + x.quantity


                return value



            def get_open(attr):
                value = 0
                rec = self.env['stock.inventory.line'].search([('inventory_id.category_id.name','=','Packing Material'),('product_id','=',attr)])
                for x in rec:
                    value = value + x.product_qty


                return value


            def get_prod(attr):
                value = 0
                rec = self.env['daily.production.tree'].search([('product.naming_type','=','finish_good'),('product.product_pack','=',attr),('daily_tree.date','<',date_from)])
                for x in rec:
                    value = value + x.qty


                return value


            def get_prod_val(attr,num):
                value = 0
                rec = self.env['daily.production.tree'].search([('product.naming_type','=','finish_good'),('product.product_pack','=',attr),('daily_tree.date','=',num)])
                for x in rec:
                    value = value + x.qty


                return value


        if types == "ctn":


            records = []
            rec = self.env['product.product'].search([('categ_id.name','=','Empty Cotton')])
            for x in rec:
                records.append(x)


            def get_purchase(attr):
                value = 0
                rec = self.env['account.invoice.line'].search([('invoice_id.type','=','in_invoice'),('product_id.naming_type','=','finish_good'),('product_id.product_pack','=',attr),('invoice_id.date_invoice','<',date_from)])
                for x in rec:
                    value = value + x.quantity


                return value


            def get_purchase_val(attr,num):
                value = 0
                rec = self.env['account.invoice.line'].search([('invoice_id.type','=','in_invoice'),('product_id.naming_type','=','finish_good'),('product_id.product_pack','=',attr),('invoice_id.date_invoice','=',num)])
                for x in rec:
                    value = value + x.quantity


                return value



            def get_open(attr):
                value = 0
                rec = self.env['stock.inventory.line'].search([('inventory_id.category_id.name','=','Empty Cotton'),('product_id','=',attr)])
                for x in rec:
                    value = value + x.product_qty


                return value


            def get_prod(attr):
                value = 0
                rec = self.env['daily.production.tree'].search([('product.naming_type','=','finish_good'),('product.product_pack','=',attr),('daily_tree.date','<',date_from)])
                for x in rec:
                    value = value + x.qty


                return value


            def get_prod_val(attr,num):
                value = 0
                rec = self.env['daily.production.tree'].search([('product.naming_type','=','finish_good'),('product.product_pack','=',attr),('daily_tree.date','=',num)])
                for x in rec:
                    value = value + x.qty


                return value



        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'dates': dates,
            'records': records,
            'get_purchase': get_purchase,
            'get_open': get_open,
            'get_prod': get_prod,
            'get_purchase_val': get_purchase_val,
            'get_prod_val': get_prod_val,
            'date_from': date_from,
            

            }

        return report_obj.render('daily_stock_report.customer_report', docargs)