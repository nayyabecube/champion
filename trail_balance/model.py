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
    _name = 'report.trail_balance.customer_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('trail_balance.customer_report')
        active_wizard = self.env['trail.balance'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list) 

        record_wizard = self.env['trail.balance'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['trail.balance'].search([('id','!=',emp_list_max)])
        record_wizard_del.unlink()


        date = record_wizard.date
        # branch = record_wizard.branch
        # b_types = record_wizard.b_types


        # if b_types == "all":
        #     branches = []
        #     rec = self.env['branch'].search([])
        #     for x in rec:
        #         branches.append(x)

        # if b_types == "specfic":
        #     branches = []
        #     for x in branch:
        #         branches.append(x)


        

        # records = []
        # def get_record(attr):
        #     del records[:]
        #     rec = self.env['account.account'].search([('user_type_id.name','!=','View_Type')])
        #     for x in rec:
        #         records.append(x)

        # def get_debit(attr,num):
        #     deb = 0
        #     rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
        #     for x in rec:
        #         deb = deb + x.debit

        #     return deb


        # def get_credit(attr,num):
        #     cre = 0
        #     rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
        #     for x in rec:
        #         cre = cre + x.credit

        #     return cre

        # def get_net(attr,num):
        #     cre = 0
        #     deb = 0
        #     net = 0
        #     rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
        #     for x in rec:
        #         cre = cre + x.credit
        #         deb = deb + x.debit

        #     net = deb - cre

        #     return abs(net)

        # if b_types == "general":
        #     branches = []
        #     for x in branch:
        #         branches.append(x)


        records = []
        rec = self.env['account.account'].search([('user_type_id.name','!=','View_Type')])
        for x in rec:
            records.append(x)

        def get_debit(num):
            deb = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
            for x in rec:
                deb = deb + x.debit

            return deb


        def get_credit(num):
            cre = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
            for x in rec:
                cre = cre + x.credit

            return cre

        def get_net(num):
            cre = 0
            deb = 0
            net = 0
            rec = self.env['account.move.line'].search([('account_id.id','=',num),('move_id.date','<=',date)])
            for x in rec:
                cre = cre + x.credit
                deb = deb + x.debit

            net = deb - cre

            return abs(net)


        # def get_num():
        #     num = 0
        #     if b_types == "general":
        #         num = 1
        #     else:
        #         num = 0

        #     return num


        

        docargs = {
        
            'doc_ids': docids,
            'doc_model': 'account.move',
            'date': date,
            'records': records,
            'get_debit': get_debit,
            'get_credit': get_credit,
            'get_net': get_net,
    
            }

        return report_obj.render('trail_balance.customer_report', docargs)