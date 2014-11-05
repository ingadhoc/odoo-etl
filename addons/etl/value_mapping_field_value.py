# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class value_mapping_field_value(osv.osv):
    """"""
    
    _name = 'etl.value_mapping_field_value'
    _description = 'value_mapping_field_value'



    _columns = {
        'ext_id': fields.char(string='Key', required=True),
        'name': fields.char(string='Help Name', required=True),
        'value_mapping_field_id': fields.many2one('etl.value_mapping_field', string='value_mapping_field_id', ondelete='cascade', required=True), 
    }

    _defaults = {
        'value_mapping_field_id': lambda self, cr, uid, context=None: context and context.get('value_mapping_field_id', False),
    }


    _constraints = [
    ]




value_mapping_field_value()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
