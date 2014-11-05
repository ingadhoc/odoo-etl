# -*- coding: utf-8 -*-

import re
from openerp import netsvc
from openerp.osv import osv, fields

class action(osv.osv):
    """"""
    
    _name = 'etl.action'
    _description = 'action'



    _columns = {
        'blocked': fields.boolean(string='Blocked'),
        'sequence': fields.integer(string='Sequence'),
        'state': fields.selection([(u'to_analyze', 'to_analyze'), (u'enabled', 'enabled'), (u'disabled', 'disabled'), (u'no_records', 'no_records')], string='State', required=True),
        'name': fields.char(string='Name', required=True),
        'source_domain': fields.char(string='Source Domain', required=True),
        'log': fields.text(string='Log'),
        'note': fields.html(string='Notes'),
        'repeating_action': fields.boolean(string='Repeating Action?'),
        'source_id_exp': fields.char(string='source_id_exp', required=True),
        'target_id_type': fields.selection([(u'source_id', 'source_id'), (u'builded_id', 'builded_id')], string='Target ID Type', required=True),
        'from_rec_id': fields.integer(string='From Record'),
        'to_rec_id': fields.integer(string='To Record'),
        'target_id_prefix': fields.char(string='target_id_prefix'),
        'manager_id': fields.many2one('etl.manager', string='Manager', ondelete='cascade', required=True), 
        'field_mapping_ids': fields.one2many('etl.field_mapping', 'action_id', string='Fields Mapping'), 
        'source_model_id': fields.many2one('etl.external_model', string='Source Model', required=True), 
        'target_model_id': fields.many2one('etl.external_model', string='Target Model'), 
    }

    _defaults = {
        'source_domain': '[]',
        'source_id_exp': 'id',
        'target_id_type': 'source_id',
        'manager_id': lambda self, cr, uid, context=None: context and context.get('manager_id', False),
    }

    _order = "sequence"

    _constraints = [
    ]




action()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
