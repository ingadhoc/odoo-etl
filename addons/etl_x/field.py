# -*- coding: utf-8 -*-
import re
from openerp import netsvc
from openerp.osv import osv, fields

class field(osv.osv):
    """"""
    
    _inherit = 'etl.field'

    def _name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('field_description', operator, name), ('name', operator, name)]
        return self.name_get(cr, name_get_uid or uid,
                             super(field, self).search(cr, uid, domain, limit=limit, context=context),
                             context=context)

    _columns = {
        'type': fields.related('model_id', 'type', type='char', string='Type', readonly=True,),
    }

    _defaults = {
    }

    _constraints = [
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
