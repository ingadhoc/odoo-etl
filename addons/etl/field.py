# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class field(osv.osv):
    """"""
    
    _name = 'etl.field'
    _description = 'field'



    _columns = {
        'name': fields.char(string='Name', required=True),
        'field_description': fields.char(string='Field Description', required=True),
        'relation': fields.char(string='Relation'),
        'relation_field': fields.char(string='Relation Field'),
        'ttype': fields.char(string='Type', required=True),
        'required': fields.char(string='Required'),
        'function': fields.char(string='Function'),
        'model_id': fields.many2one('etl.external_model', string='Model', ondelete='cascade'), 
    }

    _defaults = {
        'model_id': lambda self, cr, uid, context=None: context and context.get('model_id', False),
    }


    _constraints = [
    ]




field()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
