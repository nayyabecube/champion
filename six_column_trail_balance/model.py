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
    _name = 'report.six_column_trail_balance.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('six_column_trail_balance.customer_report')
        active_wizard = self.env['six.trailbalance'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['six.trailbalance'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['six.trailbalance'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()


        date_from = record_wizard.date_from
        date_to = record_wizard.date_to


        records = []
        rec = self.env['account.account'].search([('user_type_id.name','!=','View_Type')])
        for x in rec:
            records.append(x)


        def open_debit(attr):
            deb = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',attr),('move_id.date','<',date_from)])
            if rec:
                for x in rec:
                    deb = deb + x.debit

            return deb


        def open_cre(attr):
            cre = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',attr),('move_id.date','<',date_from)])
            if rec:
                for x in rec:
                    cre = cre + x.credit

            return cre


        def get_debit(attr):
            deb = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',attr),('move_id.date','>=',date_from),('move_id.date','<=',date_to)])
            if rec:
                for x in rec:
                    deb = deb + x.debit

            return deb


        def get_cre(attr):
            cre = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',attr),('move_id.date','>=',date_from),('move_id.date','<=',date_to)])
            if rec:
                for x in rec:
                    cre = cre + x.credit

            return cre

        def get_net(attr):
            deb = 0
            cre = 0
            debits = 0
            credits = 0
            net = 0
            netamt = 0
            total = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',attr),('move_id.date','<',date_from)])
            if rec:
                for x in rec:
                    deb = deb + x.debit
                    cre = cre + x.credit

                net = deb - cre
            record = self.env['account.move.line'].search([('account_id.id','=',attr),('move_id.date','>=',date_from),('move_id.date','<=',date_to)])
            if record:
                for y in record:
                    debits = debits + y.debit
                    credits = credits + y.credit

                netamt = debits - credits

            total = net + netamt


            return abs(total)



        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.move',
            'date_from': date_from,
            'date_to': date_to,
            'records': records,
            'open_debit': open_debit,
            'open_cre': open_cre,
            'get_cre': get_cre,
            'get_debit': get_debit,
            'get_net': get_net,
    
            }

        return report_obj.render('six_column_trail_balance.customer_report', docargs)