# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015  ADHOC SA  (http://www.adhoc.com.ar)
#    All Rights Reserved.
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
{
    'active': False,
    'author': u'ADHOC SA',
    'category': u'base.module_category_knowledge_management',
    'data': [
                u'security/etl_group.xml',
                u'view/etl_menuitem.xml',
                u'view/value_mapping_field_view.xml',
                u'view/external_model_view.xml',
                u'view/external_model_record_view.xml',
                u'view/field_mapping_view.xml',
                u'view/field_view.xml',
                u'view/action_view.xml',
                u'view/manager_view.xml',
                u'view/value_mapping_field_value_view.xml',
                u'view/value_mapping_field_detail_view.xml',
                u'data/value_mapping_field_properties.xml',
                u'data/external_model_properties.xml',
                u'data/external_model_record_properties.xml',
                u'data/field_mapping_properties.xml',
                u'data/field_properties.xml',
                u'data/manager_properties.xml',
                u'data/value_mapping_field_value_properties.xml',
                u'data/action_properties.xml',
                u'data/value_mapping_field_detail_properties.xml',
                u'data/value_mapping_field_track.xml',
                u'data/external_model_track.xml',
                u'data/external_model_record_track.xml',
                u'data/field_mapping_track.xml',
                u'data/field_track.xml',
                u'data/manager_track.xml',
                u'data/value_mapping_field_value_track.xml',
                u'data/action_track.xml',
                u'data/value_mapping_field_detail_track.xml',
                'security/ir.model.access.csv',
             ],
    'depends': ['base'],
    'description': """
odoo ETL
========
Usefull Notes:
--------------
* It is recommendend to delete all external identifiers on source database for model "res_partner" because when creating a user, odoo simulates partner creation and raise a unique constraint (excepto admin user)
* Also could be recommendend to delete external identifiers related to product and product_temlate (excepto to service product)
* Advisable to configure xmlrpc users to timezone cero to avoid errors
""",
    'installable': True,
    'application': True,
    'license': 'AGPL-3',
    'name': u'odoo ETL',
    'test': [],
    'version': u'1.1',
    'website': 'www.adhoc.com.ar'}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
