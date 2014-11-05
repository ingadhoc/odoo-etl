# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class value_mapping_field_detail(osv.osv):
    """"""
    
    _name = 'etl.value_mapping_field_detail'
    _description = 'value_mapping_field_detail'



    _columns = {
        'source_id': fields.char(string='Source ID'),
        'source_value': fields.char(string='Source Value'),
        'target_id': fields.char(string='Target ID'),
        'target_value': fields.char(string='Target Value'),
        'source_external_model_record_id': fields.many2one('etl.external_model_record', string='Source External Model Record'),
        'target_external_model_record_id': fields.many2one('etl.external_model_record', string='Target External Model Record'),
        'source_value_id': fields.many2one('etl.value_mapping_field_value', string='Source Value'),
        'target_value_id': fields.many2one('etl.value_mapping_field_value', string='Target Value'),
        'value_mapping_field_id': fields.many2one('etl.value_mapping_field', string='value_mapping_field_id', ondelete='cascade', required=True), 
    }

    _defaults = {
        'value_mapping_field_id': lambda self, cr, uid, context=None: context and context.get('value_mapping_field_id', False),
    }


    _constraints = [
    ]




value_mapping_field_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
