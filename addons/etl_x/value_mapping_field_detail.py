# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class value_mapping_field_detail(osv.osv):
    """"""
    
    _inherit = 'etl.value_mapping_field_detail'

    _columns = {
        'source_name': fields.related('source_external_model_record_id','name',type='char',string='Source Name',readonly=True,),
        'source_model_id': fields.related('value_mapping_field_id','source_model_id',type='many2one',relation='etl.external_model',string='Source Model',readonly=True,),
        'target_model_id': fields.related('value_mapping_field_id','target_model_id',type='many2one',relation='etl.external_model',string='Target Model',readonly=True,),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
