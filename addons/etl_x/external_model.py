# -*- coding: utf-8 -*-
from openerp.osv import osv
from ast import literal_eval

class external_model(osv.osv):
    """"""
    
    _inherit = 'etl.external_model'

    def _name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('model', operator, name), ('name', operator, name)]
        return self.name_get(cr, name_get_uid or uid,
                             super(external_model, self).search(cr, uid, domain, limit=limit, context=context),
                             context=context)     

    _columns = {
    }

    def read_records(self, cr, uid, ids, context=None):
        '''Function that reads external id and name field from an external model and save
        them in migrator database'''
        manager_obj = self.pool.get('etl.manager')    
        external_model_record_obj = self.pool['etl.external_model_record']
        for model in self.browse(cr, uid, ids):
            (source_connection, target_connection) = manager_obj.open_connections(cr, uid, [model.manager_id.id], context=context) 
            if model.type == 'source':
                connection = source_connection
            else:
                connection = target_connection
            
            fields_to_read = []
            if model.fields_to_read:
                fields_to_read = literal_eval(model.fields_to_read)

            record_fields = ['.id', 'id']
            record_fields.extend(fields_to_read)

            external_model_obj = connection.get_model(model.model)
            external_model_record_ids = external_model_obj.search([])
            external_model_record_data = external_model_obj.export_data(external_model_record_ids, record_fields)['datas']

            new_external_model_record_data = []
            for record in external_model_record_data:
                # take out item o and init new_record with our own ext id
                new_record = ['model' + str(model.id) + '_' + 'record_' + str(record.pop(0))] 
                # append readed external id 'id' to new record
                new_record.append(record.pop(0))
                # buid name wit readed fields
                name = ''
                while record:
                    name += str(record.pop(0)) + '; '
                # append name
                new_record.append(name)
                # append model id
                new_record.append(model.id)
                new_external_model_record_data.append(new_record)
            external_model_record_fields = ['id', 'ext_id','name','external_model_id/.id']
            # load records
            external_model_record_obj.load(cr, uid, external_model_record_fields, new_external_model_record_data)
        return True

    def read_fields_button(self, cr, uid, ids, context=None):     
        self.read_fields(cr, uid, ids, False, context=context)
        return True

    def read_fields(self, cr, uid, ids, connection=False, context=None):     
        ''' Get fields for external model ids'''
        migrator_field_obj = self.pool.get('etl.field')           
        manager_obj = self.pool.get('etl.manager')
        field_fields = ['id', 'model_id/.id', 'field_description', 'name', 'relation', 'required', 'ttype', 'function']
        model_field_data = [] 
        for model in self.browse(cr, uid, ids):
            print 'Reading fields ', model.type, ' database, model: ', model.name
            if not connection:
                (source_connection, target_connection) = manager_obj.open_connections(cr, uid, [model.manager_id.id], context=context) 
                if model.type == 'source':
                    connection = source_connection
                elif model.type == 'target':
                    connection = target_connection
                else:
                    print 'error!'
            external_model_obj = connection.get_model(model.model)
            try:
                external_model_fields = external_model_obj.fields_get()
            except:
                continue
            else:
                for field in external_model_fields:
                    field_dic = external_model_fields[field]                    
                    name = field
                    string = field_dic.get('string' or False)
                    function = field_dic.get('function' or False)
                    ttype = field_dic.get('type' or False)
                    relation = field_dic.get('relation' or False)
                    required = field_dic.get('required' or False)

                    field_data = ['field_model_' + str(model.id) + '_' + name, model.id, string, name, relation, required, ttype, function]
                    model_field_data.append(field_data)
        print 'Writing fields data...'
        migrator_field_obj.load(cr, uid, field_fields, model_field_data, context=None)

    def get_records(self, cr, uid, ids, connection, context=None):
        for record in self.browse(cr, uid, ids, context=context):
            try:
                model_obj = connection.get_model(record.model)
                model_ids = model_obj.search([])
                vals = {'records':len(model_ids)}
                print 'Cantidad de registros en clase ', record.name, ': ', len(model_ids)
                self.write(cr, uid, [record.id], vals, context=context)
            except:
                print 'error'

    def order_models(self, cr, uid, ids, context=None):
        migrator_field_obj = self.pool.get('etl.field') 
        print ('Lines to order', len(ids))
        new_order = []
        ordered_ids = []
        ordered_models = []
        models_to_order = []
        unordered_ids = ids
        order_rec = self.browse(cr, uid, ids, context=context)
        for rec in order_rec:
            models_to_order.append(rec.model)
        print 'Models_to_order', models_to_order
        count = 0
        while unordered_ids and (count<100):
            count += 1
            rec_id = unordered_ids[0]
            rec = self.browse(cr, uid, rec_id, context=context)
            print ''
            print 'Unordered_ids', unordered_ids
            model_clean_dependecies = []
            migrator_field_ids = migrator_field_obj.search(cr, uid, [('model_id','=',rec.id),('ttype','=','many2one')], context=context)
            for field in migrator_field_obj.browse(cr, uid, migrator_field_ids, context=context):
                if (field.relation not in model_clean_dependecies) and (field.relation in models_to_order):
                    if not(field.relation == rec.model):
                        model_clean_dependecies.append(field.relation)

            print 'Modelo: ',rec.model, ', depenencias: ', model_clean_dependecies
            dependecies_ok = True
            for model_dependecy in model_clean_dependecies:
                model_exception = self.check_dependency_exceptions(cr, uid, rec.model, model_dependecy, context=context)
                if (model_dependecy not in ordered_models) and not model_exception:
                    dependecies_ok = False
                    break

            unordered_ids.remove(rec_id)
            if dependecies_ok:
                print 'Dependency ok!'
                ordered_ids.append(rec.id)
                ordered_models.append(rec.model)
            else:
                print 'Break, dependency false!'
                unordered_ids.append(rec_id)

        order = 0
        print 'Unordered Models:', unordered_ids
        print 'New Order:', ordered_models
        for model_id in new_order:
            order += 10
            vals = {
                'order': order,
            }
            self.write(cr, uid, [model_id], vals, context=context)
    
    def check_dependency_exceptions(self, cr, uid, model, model_dependency, context=None):
        '''This function is for those cases where the dependency is in two ways, we add the exception so it can be ordered. 
        TODO: this is related to some fields being an exception in the model, for example, for users, you should not migrate partner (as it will be created automatically and partner don't exists before)'''

        if (model == 'res.company') and (model_dependency in ['res.partner']):    
            return True
        elif (model == 'res.users') and (model_dependency in ['res.partner','crm.case.section',]): 
            return True
        # Esto es para intentar eliminar los problemas de dependencia con ir
        elif model_dependency[3] == 'ir.': 
            return True            
        else:
            return False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
