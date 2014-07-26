# -*- coding: utf-8 -*-
{   'active': False,
    'author': u'Ingenieria ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [u'etl',],
    'description': u"""
It requires openerplib that you can get from https://pypi.python.org/pypi/openerp-client-lib/1.0.0. \n
You can install it with: \n
    pip install https://pypi.python.org/packages/source/o/openerp-client-lib/openerp-client-lib-1.0.0.tar.gz
    """,
    'init_xml': [],
    'installable': True,
    'license': 'AGPL-3',
    'name': u'odoo ELT Project',
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
    'website': 'www.ingadhoc.com'}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
