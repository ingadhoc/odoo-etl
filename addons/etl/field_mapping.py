# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class field_mapping(osv.osv):
    """"""
    
    _name = 'etl.field_mapping'
    _description = 'field_mapping'



    _columns = {
        'blocked': fields.boolean(string='Blocked'),
        'state': fields.selection([(u'on_repeating', 'on_repeating'), (u'to_analyze', 'to_analyze'), (u'enabled', 'enabled'), (u'disabled', 'disabled'), (u'other_class', 'other_class')], string='State', required=True),
        'type': fields.selection([(u'field', 'field'), (u'expression', 'expression'), (u'migrated_id', u'Migrated ID'), (u'value_mapping', u'Value Mapping'), (u'date_adapt', u'Date Adapt'), (u'reference', 'reference')], string='Source Type'),
        'source_field_id': fields.many2one('etl.field', string='Source Field'),
        'source_field': fields.char(string='Source Exp.'),
        'target_field_id': fields.many2one('etl.field', string='Target Field'),
        'target_field': fields.char(string='Target Exp.'),
        'expression': fields.text(string='Expression'),
        'value_mapping_field_id': fields.many2one('etl.value_mapping_field', string='Value Mapping Field'),
        'model_field_id': fields.many2one('etl.field', string='Model Field'),
        'model_field': fields.char(string='Model Field Exp.'),
        'note': fields.html(string='Notes'),
        'action_id': fields.many2one('etl.action', string='Action', ondelete='cascade', required=True), 
    }

    _defaults = {
        'blocked': False,
        'expression': "context['result']= False",
        'type': 'field',
        'action_id': lambda self, cr, uid, context=None: context and context.get('action_id', False),
    }


    _constraints = [
    ]




field_mapping()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
