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


{   'active': False,
    'author': u'Sistemas ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [u'mail', u'contacts'],
    'description': u'OpenERP Migrator',
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'OpenERP Migrator',
    'test': [],
    'update_xml': [   u'security/oerp_migrator_group.xml',
                      u'view/value_mapping_field_view.xml',
                      u'view/external_model_view.xml',
                      u'view/external_model_record_view.xml',
                      u'view/field_mapping_view.xml',
                      u'view/field_view.xml',
                      u'view/manager_view.xml',
                      u'view/value_mapping_field_value_view.xml',
                      u'view/action_view.xml',
                      u'view/value_mapping_field_detail_view.xml',
                      u'view/oerp_migrator_menuitem.xml',
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
                      'security/ir.model.access.csv'],
    'version': u'1.1',
    'website': ''}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
