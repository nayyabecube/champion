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

class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.register_payment.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('register_payment.customer_report')
        active_wizard = self.env['reg.payment'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['reg.payment'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['reg.payment'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to

        enteries = []
        records = self.env['account.invoice.line'].search([('invoice_id.type','=','in_invoice'),('invoice_id.date_invoice','>=',record_wizard.date_from),('invoice_id.date_invoice','<=',record_wizard.date_to)])
        for x in records:
            enteries.append(x)

        enteries.sort(key=lambda x: x.invoice_id.date_invoice)



        count = 1
        
        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': enteries,
            'date':date,
            'count':count,

            }

        return report_obj.render('register_payment.customer_report', docargs)