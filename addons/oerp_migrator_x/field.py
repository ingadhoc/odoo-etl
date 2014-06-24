# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Migrator
#    Copyright (C) 2013 Sistemas ADHOC
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
    
    _inherit = 'oerp_migrator.field'

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
