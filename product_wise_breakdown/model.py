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
    _name = 'report.product_wise_breakdown.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('product_wise_breakdown.customer_report')
        active_wizard = self.env['productwise.breakdown'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['productwise.breakdown'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['productwise.breakdown'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to



        d1 = datetime.datetime.strptime(record_wizard.date_from, "%Y-%m-%d")
        d2 = datetime.datetime.strptime(record_wizard.date_to, "%Y-%m-%d")

        delta = d2 - d1
        dates = []
        for i in range(delta.days + 1):
            dates.append((d1 + timedelta(days=i)).strftime('%Y-%m-%d'))




        records = []
        def get_prod(attr):
            del records [:]
            rec = self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice'),('invoice_id.date_invoice','=',attr)])
            for x in rec:
                if x.product_id not in records:
                    records.append(x.product_id)



        enteries = []
        count = 0
        rec = self.env['product.receipe.tree'].search([])
        for x in rec:
            if x.product:
                if x.product not in enteries:
                    count = count + 1
                    enteries.append(x.product)



        def get_qty(attr,num):
            value = 0
            rec = self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice'),('invoice_id.date_invoice','=',attr),('product_id','=',num)])
            for x in rec:
                value = value + x.quantity

            return value


        def get_recp(attr,num,recep):
            value = 0
            rec = self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice'),('invoice_id.date_invoice','=',attr),('product_id','=',num)])
            for x in rec:
                if x.product_id.product_receipe.receipe_id:
                    for y in x.product_id.product_receipe.receipe_id:
                        if y.product.id == recep:
                            value = y.ratio


            return value



        def get_tot(attr,num):
            get_prod(attr)
            total = 0
            for x in records:
                total = total + get_recp(attr,x.id,num)

            return total

        def get_size(attr,num):
            n = 0
            rec = self.env['account.invoice.line'].search([('invoice_id.type','=','out_invoice'),('invoice_id.date_invoice','=',attr),('product_id','=',num)])
            for x in rec:
                if x.product_id.attribute_value_ids:
                    for y in x.product_id.attribute_value_ids:
                        if y.attribute_id.name == "Size" or y.attribute_id.name == "size":
                            if re.findall(r"[-+]?\d*\.\d+|\d+", y.name):
                                n = float(re.findall("[-+]?\d*\.\d+|\d+", y.name)[0])


            return n



        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'dates': dates,
            'records': records,
            'get_prod': get_prod,
            'get_qty': get_qty,
            'get_size': get_size,
            'enteries': enteries,
            'number': count,
            'get_recp': get_recp,
            'get_tot': get_tot,

            }

        return report_obj.render('product_wise_breakdown.customer_report', docargs)