# -*- coding: utf-8 -*-
##############################################################################
#
#    Saas Manager
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


{   'active': False,
    'author': u'Sistemas ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [u'oerp_migrator',],
    'description': u"""
    Require openerplib que se obtiene de https://pypi.python.org/pypi/openerp-client-lib/1.0.0 y se puede instalar con:
    sudo oerpenv pip install https://pypi.python.org/packages/source/o/openerp-client-lib/openerp-client-lib-1.0.0.tar.gz#md5=5aca790999472cf3488eb6bf71606d98
    """,
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'Oerp Migrator Project',
    'test': [],
    'update_xml': [ 
                'view/manager_view.xml',  
                'view/field_mapping_view.xml',
                'view/field_view.xml',
                'view/action_view.xml',
                'view/external_model_view.xml',
                'view/value_mapping_field_view.xml',
                'view/value_mapping_field_detail_view.xml',
                  ],
    'version': u'1.1',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
