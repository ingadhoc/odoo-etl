# -*- coding: utf-8 -*-

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
        'workflow_models': fields.char(string='Models to delete Workflows', required=True),
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
