# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
import time
from openerp.tools.safe_eval import safe_eval as eval
from openerp.tools.translate import _

class field_mapping(osv.osv):
    """"""
    
    _inherit = 'etl.field_mapping'

    _columns = {
        'target_model_id': fields.related(
                    'action_id',
                    'target_model_id',
                    type='many2one',
                    relation='etl.external_model',
                    string='target_model_id'
                    ),
        'source_model_id': fields.related(
                    'action_id',
                    'source_model_id',
                    type='many2one',
                    relation='etl.external_model',
                    string='target_model_id'
                    ),        
        'source_field_ttype': fields.related(
                    'source_field_id',
                    'ttype',
                    type='char',
                    readonly=True,
                    string='Source Type'
                    ), 
        'target_field_ttype': fields.related(
                    'target_field_id',
                    'ttype',
                    type='char',
                    readonly=True,
                    string='Source Type'
                    ),      
        'manager_id': fields.related(
                    'action_id',
                    'manager_id',
                    type='many2one',
                    relation='etl.manager',                    
                    readonly=True,
                    string='Manager'
                    ),                               
    }

    def get_migrated_id(self, cr, uid, ids, rec_id, source_connection=False, target_connection=False, context=None):
        '''Get migrated id for field ids  and one rec_id (from source database)
        For example, for field mapping ids'''
        if context is None:
            context = {}
        result = []
        
        for field_mapping in self.browse(cr, uid, ids, context=context):
            if not source_connection or not target_connection:
                (source_connection, target_connection) = self.pool.get('etl.manager').open_connections(cr, uid, [field_mapping.action_id.manager_id.id], context=context)
            source_model_obj = source_connection.get_model(field_mapping.action_id.source_model_id.model)
            # target_model_obj = target_connection.get_model(field_mapping.action_id.target_model_id.model)    
            target_ir_model_data_obj = target_connection.get_model('ir.model.data')
            source_fields = ['id',field_mapping.source_field_id.name, field_mapping.model_field_id.name]
            source_model_data = source_model_obj.export_data([rec_id], source_fields)['datas']
            target_id = False
            if source_model_data:
                source_id = source_model_data[0][1]
                source_resource_obj = source_connection.get_model(source_model_data[0][2])
                source_reference = source_resource_obj.export_data([source_id],['id'])['datas']
                if source_reference[0]:
                    source_reference_splited = source_reference[0][0].split('.', 1)
                    if len(source_reference_splited) == 1:
                        module = False
                        external_ref = source_reference_splited[0] 
                    else:
                        module = source_reference_splited[0]
                        external_ref = source_reference_splited[1]                
                    target_id = target_ir_model_data_obj.get_object_reference(module, external_ref)[1]
            result.append(target_id)
        return result

    def run_expressions(self, cr, uid, ids, rec_id, source_connection=False, target_connection=False, context=None):
        if context is None:
            context = {}
        user = self.pool.get('res.users').browse(cr, uid, uid)
        result = []
        
        for field_mapping in self.browse(cr, uid, ids, context=context):
            expression_result = False
            if not source_connection or not target_connection:
                (source_connection, target_connection) = self.pool.get('etl.manager').open_connections(cr, uid, [field_mapping.action_id.manager_id.id], context=context)
            source_model_obj = source_connection.get_model(field_mapping.action_id.source_model_id.model)    
            target_model_obj = target_connection.get_model(field_mapping.action_id.target_model_id.model)    
            
            obj_pool = source_model_obj
            cxt = {
                'self': obj_pool, #to be replaced by target_obj
                'source_obj': source_model_obj,
                'source_connection': source_connection,
                'target_obj': target_model_obj,
                'target_connection': target_connection,
                'rec_id': rec_id,
                'pool': self.pool,
                'time': time,
                'cr': cr,
                'context': dict(context), # copy context to prevent side-effects of eval
                'uid': uid,
                'user': user,
            }
            if not field_mapping.expression:
                raise osv.except_osv(_('Warning!'),_('Type expression choosen buy not expression set'))
            eval(field_mapping.expression.strip(), cxt, mode="exec") # nocopy allows to return 'action'
            if 'result' in cxt['context']:
                expression_result = cxt['context'].get('result')
            result.append(expression_result)
        return result

    def onchange_source_field_id(self, cr, uid, ids, source_field_id, context=None):
        v = {}
        if source_field_id:
            migrator_field_obj = self.pool.get('etl.field')
            migrator_field_rec = migrator_field_obj.browse(cr, uid, source_field_id, context=context)
            
            if not migrator_field_rec:
                return {'value': v}
            
            if isinstance(migrator_field_rec, list):
                migrator_field_rec = migrator_field_rec[0]
            if migrator_field_rec.ttype == 'many2one':
                v['source_field'] = migrator_field_rec.name + '/id'
            else:            
                v['source_field'] = migrator_field_rec.name
        else:
            v['source_field'] = False
       
        return {'value': v}        

    def onchange_target_field_id(self, cr, uid, ids, target_field_id, context=None):
        v = {}
        if target_field_id:
            migrator_field_obj = self.pool.get('etl.field')
            migrator_field_rec = migrator_field_obj.browse(cr, uid, target_field_id, context=context)
            
            if not migrator_field_rec:
                return {'value': v}
            
            if isinstance(migrator_field_rec, list):
                migrator_field_rec = migrator_field_rec[0]
            if migrator_field_rec.ttype == 'many2one':
                v['target_field'] = migrator_field_rec.name + '/id'
            else:
                v['target_field'] = migrator_field_rec.name
        else:
            v['target_field'] = False
       
        return {'value': v}        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
