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

class field_mapping(osv.osv):
    """"""
    
    _name = 'etl.field_mapping'
    _description = 'field_mapping'

    _columns = {
        'blocked': fields.boolean(string='Blocked'),
        'state': fields.selection([(u'on_repeating', 'on_repeating'), (u'to_analyze', 'to_analyze'), (u'enabled', 'enabled'), (u'disabled', 'disabled'), (u'other_class', 'other_class')], string='State', required=True),
        'type': fields.selection([(u'field', 'field'), (u'expression', 'expression'), (u'migrated_id', u'Migrated ID'), (u'value_mapping', u'Value Mapping'), (u'date_adapt', u'Date Adapt')], string='Source Type'),
        'source_field_id': fields.many2one('etl.field', string='Source Field'),
        'source_field': fields.char(string='Source Exp.'),
        'target_field_id': fields.many2one('etl.field', string='Target Field'),
        'target_field': fields.char(string='Target Exp.'),
        'expression': fields.text(string='Expression'),
        'value_mapping_field_id': fields.many2one('etl.value_mapping_field', string='Value Mapping Field'),
        'model_field_id': fields.many2one('etl.field', string='Model Field'),
        'note': fields.html(string='Notes'),
        'action_id': fields.many2one('etl.action', string='Action', ondelete='cascade', required=True), 
    }

    _defaults = {
        'blocked': False,
        'expression': "context['result']= False",
        'type': 'field',
    }


    _constraints = [
    ]




field_mapping()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
