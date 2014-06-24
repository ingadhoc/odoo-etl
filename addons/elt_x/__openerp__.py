# -*- coding: utf-8 -*-
{   'active': False,
    'author': u'Ingenieria ADHOC',
    'category': u'base.module_category_knowledge_management',
    'demo_xml': [],
    'depends': [u'elt',],
    'description': u"""
    Require openerplib que se obtiene de https://pypi.python.org/pypi/openerp-client-lib/1.0.0 y se puede instalar con:
    sudo oerpenv pip install https://pypi.python.org/packages/source/o/openerp-client-lib/openerp-client-lib-1.0.0.tar.gz#md5=5aca790999472cf3488eb6bf71606d98
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
