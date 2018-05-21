# -*- coding: utf-8 -*-
import re
from openerp import models, fields, api
from openerp.osv import fields, osv
import requests


class solt_http_test(osv.osv):
    _name = 'solt.http.test'
    
    _columns = {
        'name': fields.char('URL', size=1024),
        'method': fields.selection([('post', 'POST'), ('get', 'GET'), ('put', 'PUT'), ('patch', 'PATCH'), ('delete', 'DELETE')], string='HTTP Method'),
        'user': fields.char('User', size=64),
        'password': fields.char('Password', size=64),
        'content': fields.text('Content'),
        'response': fields.text('Response'),
    }
    
    def action_request(self, cr, uid, ids, context=None):
        for test in self.browse(cr, uid, ids,context):
            auth = None
            if test.user and test.password:
                auth = (test.user,test.password)
            headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
            result = getattr(requests, test.method)(test.name, test.content, auth=auth, headers=headers)
            test.write({'response':result.text})
        return True

        
solt_http_test()


















