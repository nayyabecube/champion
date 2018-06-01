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

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.champ_sales_invoice.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('champ_sales_invoice.module_report')
        records = self.env['account.invoice'].browse(docids)

        enteries = []
        for x in records.invoice_line_ids:
            enteries.append(x)

        lists = []
        for y in records.tax_line_ids:
            if "Sales" in y.name:
                pass
            else:
                lists.append(y)

        def sales():
            varriant = []
            for x in enteries:
                for y in x.product_id:
                    for z in y.attribute_value_ids:
                        varriant.append(z.name)
                        print varriant
                        print "kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"

        print sales()


        def price():
            numb = 0
            for data in records.invoice_line_ids:
                if data.discount:
                    numb = data.discount

                return int(numb)

        def rate(product):
            products = self.env["product.product"].search([('id','=',product)])
            for x in products.attribute_value_ids:
                if x.attribute_id.name == "Size":
                    return x.name
                if x.attribute_id.name == "Volume":
                    return x.name

        def percent():
            value = 0
            new = 0
            for x in records.invoice_line_ids:
                for y in x.invoice_line_tax_ids:
                    value = y.name
                    if "Sales" in value:
                        taxes = self.env["account.tax"].search([('name','=',value)])
                        new = taxes.amount
                    else:
                        new = 0

            return new




                    
                           

        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'data': data,
            'enteries': enteries,
            'lists': lists,
            'sales': sales,
            'price': price,
            'rate': rate,
            'percent': percent
            }

        return report_obj.render('champ_sales_invoice.module_report', docargs)