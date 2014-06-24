# -*- coding: utf-8 -*-
from openerp.osv import osv

class value_mapping_field(osv.osv):
    """"""
    
    _inherit = 'oerp_migrator.value_mapping_field'

    _columns = {
    }

    def map_record(self, cr, uid, ids, context=None):
        value_mapping_field_detail_obj = self.pool.get('oerp_migrator.value_mapping_field_detail')        
        external_model_record_obj = self.pool['oerp_migrator.external_model_record']
        for record in self.browse(cr, uid, ids):
            value_mapping_data = []
            for source_record in record.source_model_id.external_model_record_ids:
                domain = [('external_model_id','=', record.target_model_id.id),
                    ('name','ilike',source_record.name)]
                target_record_ids = external_model_record_obj.search(cr, uid, domain, context=context)
                target_record_id = False
                if target_record_ids:
                    target_record_id = target_record_ids[0]
                value_mapping_data.append([
                    'value_mapping_' + str(source_record.id),
                    source_record.id,
                    target_record_id,
                    record.id,
                    ])

            value_mapping_fields = ['id','source_external_model_record_id/.id', 'target_external_model_record_id/.id', 'value_mapping_field_id/.id']
            import_result = value_mapping_field_detail_obj.load(cr, uid, value_mapping_fields, value_mapping_data)
            vals = {'log':import_result}
            # write log and domain if active field exist
            self.write(cr, uid, [record.id], vals, context=context)
        return True        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
