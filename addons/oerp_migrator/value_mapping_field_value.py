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

class value_mapping_field_value(osv.osv):
    """"""
    
    _name = 'oerp_migrator.value_mapping_field_value'
    _description = 'value_mapping_field_value'

    _columns = {
        'ext_id': fields.char(string='Key', required=True),
        'name': fields.char(string='Help Name', required=True),
        'value_mapping_field_id': fields.many2one('oerp_migrator.value_mapping_field', string='value_mapping_field_id', ondelete='cascade', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




value_mapping_field_value()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
