# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Migrator
#    Copyright (C) 2014 Sistemas ADHOC
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

class value_mapping_field_detail(osv.osv):
    """"""
    
    _name = 'oerp_migrator.value_mapping_field_detail'
    _description = 'value_mapping_field_detail'

    _columns = {
        'source_id': fields.char(string='Source ID'),
        'source_value': fields.char(string='Source Value'),
        'target_id': fields.char(string='Target ID'),
        'target_value': fields.char(string='Target Value'),
        'source_external_model_record_id': fields.many2one('oerp_migrator.external_model_record', string='Source External Model Record'),
        'target_external_model_record_id': fields.many2one('oerp_migrator.external_model_record', string='Target External Model Record'),
        'source_value_id': fields.many2one('oerp_migrator.value_mapping_field_value', string='Source Value'),
        'target_value_id': fields.many2one('oerp_migrator.value_mapping_field_value', string='Target Value'),
        'value_mapping_field_id': fields.many2one('oerp_migrator.value_mapping_field', string='value_mapping_field_id', ondelete='cascade', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




value_mapping_field_detail()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
