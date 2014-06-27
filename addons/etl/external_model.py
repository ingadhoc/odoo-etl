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

class external_model(osv.osv):
    """"""
    
    _name = 'etl.external_model'
    _description = 'external_model'

    _columns = {
        'sequence': fields.integer(string='Sequence', readonly=True),
        'type': fields.selection([(u'source', u'Source'), (u'target', u'Target')], string='Type', readonly=True, required=True),
        'name': fields.char(string='Name', readonly=True, required=True),
        'model': fields.char(string='Model', readonly=True, required=True),
        'order': fields.integer(string='Order', readonly=True),
        'records': fields.integer(string='Records', readonly=True),
        'fields_to_read': fields.char(string='Fields to read'),
        'field_ids': fields.one2many('etl.field', 'model_id', string='Fields', readonly=True), 
        'source_action_ids': fields.one2many('etl.action', 'source_model_id', string='source_action_ids'), 
        'target_action_ids': fields.one2many('etl.action', 'target_model_id', string='target_action_ids'), 
        'manager_id': fields.many2one('etl.manager', string='Manager', readonly=True, ondelete='cascade', required=True), 
        'external_model_record_ids': fields.one2many('etl.external_model_record', 'external_model_id', string='external_model_record_ids'), 
    }

    _defaults = {
        'fields_to_read': ['name'],
    }

    _order = "sequence"

    _constraints = [
    ]




external_model()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
