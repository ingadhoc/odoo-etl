# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class value_mapping_field(osv.osv):
    """"""
    
    _name = 'etl.value_mapping_field'
    _description = 'value_mapping_field'



    _columns = {
        'name': fields.char(string='Field Name', required=True),
        'type': fields.selection([(u'id', u'Id'), (u'char', u'Char (not implemented yet)'), (u'selection', u'Selection')], string='Type', required=True),
        'source_model_id': fields.many2one('etl.external_model', string='Source Model'),
        'target_model_id': fields.many2one('etl.external_model', string='Target Model'),
        'log': fields.text(string='log'),
        'value_mapping_field_detail_ids': fields.one2many('etl.value_mapping_field_detail', 'value_mapping_field_id', string='Details'), 
        'value_mapping_field_value_ids': fields.one2many('etl.value_mapping_field_value', 'value_mapping_field_id', string='Mapping Values'), 
        'manager_id': fields.many2one('etl.manager', string='manager_id', ondelete='cascade', required=True), 
    }

    _defaults = {
        'manager_id': lambda self, cr, uid, context=None: context and context.get('manager_id', False),
    }


    _constraints = [
    ]




value_mapping_field()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
