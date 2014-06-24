# -*- coding: utf-8 -*-
##############################################################################
#
#    odoo ELT
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

class action(osv.osv):
    """"""
    
    _name = 'elt.action'
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
        'target_id_exp': fields.char(string='target_id_exp', required=True),
        'from_rec_id': fields.integer(string='From Record'),
        'to_rec_id': fields.integer(string='To Record'),
        'manager_id': fields.many2one('elt.manager', string='Manager', ondelete='cascade', required=True), 
        'field_mapping_ids': fields.one2many('elt.field_mapping', 'action_id', string='Fields Mapping'), 
        'source_model_id': fields.many2one('elt.external_model', string='Source Model', required=True), 
        'target_model_id': fields.many2one('elt.external_model', string='Target Model'), 
    }

    _defaults = {
        'source_domain': '[]',
        'source_id_exp': 'id',
        'target_id_exp': 'id',
    }

    _order = "sequence"

    _constraints = [
    ]




action()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
