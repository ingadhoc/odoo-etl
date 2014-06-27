# -*- coding: utf-8 -*-
##############################################################################
#
#    odoo ETL
#    Copyright (C) 2014 Ingenieria ADHOC
#    No email
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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


import re
from openerp import netsvc
from openerp.osv import osv, fields

class manager(osv.osv):
    """"""
    
    _name = 'etl.manager'
    _description = 'manager'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'source_hostname': fields.char(string='Source Hostname', required=True),
        'source_port': fields.integer(string='Source Port', required=True),
        'source_database': fields.char(string='Source Database', required=True),
        'source_login': fields.char(string='Source Login', required=True),
        'source_password': fields.char(string='Source Password', required=True),
        'target_hostname': fields.char(string='Target Hostname', required=True),
        'target_port': fields.integer(string='Target Port', required=True),
        'target_database': fields.char(string='Target Database', required=True),
        'target_login': fields.char(string='Target Login', required=True),
        'target_password': fields.char(string='Target Password', required=True),
        'log': fields.text(string='Log'),
        'model_disable_default': fields.text(string='Models Disabled by Default'),
        'field_disable_default': fields.text(string='Fields Disable by Default'),
        'model_exception_words': fields.char(string='Model Exception Words'),
        'model_analyze_default': fields.text(string='Models Analyze by Default'),
        'note': fields.html(string='Notes'),
        'field_analyze_default': fields.text(string='Fields Analize by Default'),
        'repeating_models': fields.text(string='Repeating Models'),
        'field_disable_words': fields.text(string='Fields Disable by Default Words'),
        'modules_to_install': fields.text(string='Modules To Install'),
        'workflow_models': fields.char(string='Workflow Models', required=True),
        'action_ids': fields.one2many('etl.action', 'manager_id', string='Actions', domain=[('state','in',['to_analyze','enabled'])]), 
        'external_model_ids': fields.one2many('etl.external_model', 'manager_id', string='External Models', readonly=True), 
        'value_mapping_field_ids': fields.one2many('etl.value_mapping_field', 'manager_id', string='Value Mapping Fields'), 
    }

    _defaults = {
        'modules_to_install': [],
        'workflow_models': '[]',
    }


    _constraints = [
    ]


    def open_connections(self, cr, uid, ids, context=None):
        """"""
        raise NotImplementedError



manager()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
