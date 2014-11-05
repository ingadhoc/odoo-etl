# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class external_model_record(osv.osv):
    """"""
    
    _name = 'etl.external_model_record'
    _description = 'external_model_record'



    _columns = {
        'ext_id': fields.char(string='Value To be Mapped', required=True),
        'name': fields.char(string='Help Name', required=True),
        'external_model_id': fields.many2one('etl.external_model', string='external_model_id', ondelete='cascade', required=True), 
    }

    _defaults = {
        'external_model_id': lambda self, cr, uid, context=None: context and context.get('external_model_id', False),
    }


    _constraints = [
    ]




external_model_record()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
