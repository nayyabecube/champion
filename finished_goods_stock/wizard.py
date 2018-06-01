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
from datetime import timedelta,datetime,date
from dateutil.relativedelta import relativedelta


class RegionWiseDetail(models.Model):
    _name = "finished.goods"

    date = fields.Date("Date",required=True)
    prev = fields.Date("Date")

    @api.onchange('date')
    def select_date(self):
        if self.date:
            start_date = datetime.strptime(self.date,"%Y-%m-%d")
            self.prev = start_date - relativedelta(months=1)


class regionWiseDetail(models.Model):
    _inherit = "daily.production"    

    @api.multi
    def create_report(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Customer Profile',
        'res_model': 'finished.goods',
        'view_type': 'form',
        'view_mode': 'form',
        'target' : 'new',
        }
    
    
