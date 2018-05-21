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
    _name = 'report.finished_goods_stock.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('finished_goods_stock.customer_report')
        active_wizard = self.env['finished.goods'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['finished.goods'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['finished.goods'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date = record_wizard.date
        prev = record_wizard.prev


        
        parent_category = []
        category = self.env['product.category'].search([('finish_good','=',True)])
        for x in category:
            if x.parent_id not in parent_category:
                parent_category.append(x.parent_id)


        def month_lit(attr):
            current_month = str(date[:7])
            value = 0
            daily = self.env['daily.production.tree'].search([('product.categ_id.finish_good','=',True),('product.categ_id.parent_id','=',attr)])
            for y in daily:
                if y.date:
                    if str(y.date[:7]) == current_month:
                        value = value + y.qty_lit

            return value

        def last_lit(attr):
            last_month = str(prev[:7])
            value = 0
            daily = self.env['daily.production.tree'].search([('product.categ_id.finish_good','=',True),('product.categ_id.parent_id','=',attr)])
            for y in daily:
                if y.date:
                    if str(y.date[:7]) == last_month:
                        value = value + y.qty_lit

            return value

        def month_kg(attr):
            current_month = str(date[:7])
            value = 0
            daily = self.env['daily.production.tree'].search([('product.categ_id.finish_good','=',True),('product.categ_id.parent_id','=',attr)])
            for y in daily:
                if y.date:
                    if str(y.date[:7]) == current_month:
                        value = value + y.qty_kg

            return value


        def last_kg(attr):
            last_month = str(prev[:7])
            value = 0
            daily = self.env['daily.production.tree'].search([('product.categ_id.finish_good','=',True),('product.categ_id.parent_id','=',attr)])
            for y in daily:
                if y.date:
                    if str(y.date[:7]) == last_month:
                        value = value + y.qty_kg

            return value


        category = self.env['product.category'].search([('finish_good','=',True)])

        sizes = []
        def get_size(attr):
            del sizes[:]
            prod_temp = self.env['product.template'].search([('categ_id.finish_good','=',True),('categ_id','=',attr)])
            for x in prod_temp:
                for y in x.attribute_line_ids:
                    if y.attribute_id.name == 'Size':
                        for z in y.attribute_id.value_ids:
                            if "Litre" in str(z.name) or "Ltr" in str(z.name) or "Lt" in str(z.name):
                                if re.findall(r"[-+]?\d*\.\d+|\d+", z.name):
                                    n = float(re.findall("[-+]?\d*\.\d+|\d+", z.name)[0])
                                    if n not in sizes:
                                        sizes.append(n)





        def get_value(attr,num):
            current_month = str(date[:7])
            value = 8
            products = []
            prod_temp = self.env['product.template'].search([('categ_id.finish_good','=',True),('categ_id','=',attr)])
            for x in prod_temp:
                for y in x.attribute_line_ids:
                    if y.attribute_id.name == 'Size':
                        for z in y.attribute_id.value_ids:
                            if "Litre" in str(z.name) or "Ltr" in str(z.name) or "Lt" in str(z.name):
                                if re.findall(r"[-+]?\d*\.\d+|\d+", z.name):
                                    n = float(re.findall("[-+]?\d*\.\d+|\d+", z.name)[0])
                                    if n == num:
                                        if x not in products:
                                            products.append(x)


            for z in products:
                daily = self.env['daily.production.tree'].search([('product.categ_id.finish_good','=',True),('product.categ_id','=',attr),('product.product_tmpl_id','=',z.id)])
                for y in daily:
                    if daily:
                        if y.date:
                            if str(y.date[:7]) == current_month:
                                value = value + y.qty_lit

            return value



        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'daily.production',
            'category':category,
            'sizes':sizes,
            'get_size':get_size,
            'get_value':get_value,
            'parent_category':parent_category,
            'month_lit':month_lit,
            'month_kg':month_kg,
            'last_lit':last_lit,
            'last_kg':last_kg,
            'date':date,
            'prev':prev,

            }

        return report_obj.render('finished_goods_stock.customer_report', docargs)