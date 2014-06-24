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

class field(osv.osv):
    """"""
    
    _name = 'elt.field'
    _description = 'field'

    _columns = {
        'name': fields.char(string='Name', required=True),
        'field_description': fields.char(string='Field Description', required=True),
        'relation': fields.char(string='Relation'),
        'relation_field': fields.char(string='Relation Field'),
        'ttype': fields.char(string='Type', required=True),
        'required': fields.char(string='Required'),
        'function': fields.char(string='Function'),
        'model_id': fields.many2one('elt.external_model', string='Model', ondelete='cascade'), 
    }

    _defaults = {
    }


    _constraints = [
    ]




field()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
