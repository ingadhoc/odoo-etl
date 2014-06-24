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

class external_model_record(osv.osv):
    """"""
    
    _name = 'elt.external_model_record'
    _description = 'external_model_record'

    _columns = {
        'ext_id': fields.char(string='Value To be Mapped', required=True),
        'name': fields.char(string='Help Name', required=True),
        'external_model_id': fields.many2one('elt.external_model', string='external_model_id', ondelete='cascade', required=True), 
    }

    _defaults = {
    }


    _constraints = [
    ]




external_model_record()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
