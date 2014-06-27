# -*- coding: utf-8 -*-
import sys
from openerp.osv import osv, fields
from ast import literal_eval
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp import SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

class action(osv.osv):
    """"""
    
    _inherit = 'etl.action'

    _columns = {
        'source_records': fields.related(
                    'source_model_id',
                    'records',
                    type='integer',
                    readonly=True,
                    string='Source Records'
                    ), 
        'target_records': fields.related(
                    'target_model_id',
                    'records',
                    type='integer',
                    readonly=True,
                    string='Target Records'
                    ),     
        'source_model_id': fields.many2one('etl.external_model', ondelete='cascade', string='source_model_id', required=True), 
        'target_model_id': fields.many2one('etl.external_model', ondelete='cascade', string='target_model_id'),         
    }

    _defaults = {
    }


    _constraints = [
    ]

    def copy(self, cr, uid, id, default=None, context=None):
        if not context:
            context = {}
        default.update({
            'field_mapping_ids': False,
            'blocked': False,
            'repeating_action': False,
            })
        return super(action, self).copy(cr, uid, id, default, context)     

    def match_fields(self, cr, uid, ids, context=None):
        ''' Mach fields'''
        migrator_field_obj = self.pool.get('etl.field') 
        field_mapping_obj = self.pool.get('etl.field_mapping')        
        
        for action in self.browse(cr, uid, ids):
            repeating_action = False
            # Get disabled and to analize words and fields
            field_disable_default = []
            field_analyze_default = []
            field_disable_words = []
            if action.manager_id.field_disable_default:
                field_disable_default = literal_eval(action.manager_id.field_disable_default)
            if action.manager_id.field_analyze_default:
                field_analyze_default = literal_eval(action.manager_id.field_analyze_default) 
            if action.manager_id.field_disable_words:
                field_disable_words = literal_eval(action.manager_id.field_disable_words) 

            # get source fields thar are not functions ore one2many
            source_domain = [('model_id.id','=',action.source_model_id.id),('ttype','not in', ['one2many']),'|',('function','=', False),('required','=', 'True')]
            source_field_ids = migrator_field_obj.search(cr, uid, source_domain, context=context)
            
            mapping_data = []            
            action_has_active_field = False
            for field in migrator_field_obj.browse(cr, uid, source_field_ids, context=context):
                # If nothing asserts, choose expresion
                mapping_type = 'expression'
                
                # build source_field with or not /id
                source_field = field.name
                if field.ttype in ['many2one','many2many']:
                    source_field += '/id'

                # look for a target field
                target_domain = [('model_id.id','=',action.target_model_id.id),('name','=',field.name)]
                target_fields_ids = migrator_field_obj.search(cr, uid, target_domain, context=context)

                # check the state
                state = 'enabled'
                if field.name in field_analyze_default or not target_fields_ids:
                    state = 'to_analyze'                    
                if field.name in field_disable_default:
                    state = 'disabled'
                else:
                    for field_disable_word in field_disable_words:
                        if field.name.find(field_disable_word) == 0:
                            state = 'disabled'
                
                # check if is active field
                if field.name == 'active':
                    action_has_active_field = True

                # depending on the target field properties, set some other values
                target_field = ''
                target_field_id = False
                if target_fields_ids:
                    mapping_type = 'field'
                    target_field_id = target_fields_ids[0]
                    target_field_rec = migrator_field_obj.browse(cr, uid, target_field_id, context=context)

                    target_field = target_field_rec.name
                    if target_field_rec.ttype in ['many2one','many2many']:
                        target_field += '/id'
                        if target_field_rec.ttype == 'many2many':
                            relation = target_field_rec.relation
                            previus_action_ids = self.search(cr, uid, [('manager_id','=',action.manager_id.id),('sequence','<',action.sequence),('target_model_id.model','=',relation)], context=context)
                            if not previus_action_ids:
                                state = 'other_class'
                    elif field.ttype == 'datetime' and target_field_rec.ttype == 'date' or field.ttype == 'date' and target_field_rec.ttype == 'datetime':
                        mapping_type = 'date_adapt'

                # Check if there is any value mapping for current field
                value_mapping_field_id = False
                value_mapping_ids = self.pool['etl.value_mapping_field'].search(cr, uid, [('name','=',field.name),('manager_id','=',action.manager_id.id)], context=context)
                if value_mapping_ids:
                    mapping_type = 'value_mapping'
                    value_mapping_field_id = value_mapping_ids[0]

                # If field name = 'state' then we upload it on a repeating action so we are sure we can upload all the related data
                if field.name == 'state':
                    state = 'on_repeating'
                    repeating_action = True
                vals = ['field_mapping_' + str(action.id) + '_' + str(field.id), state, field.id, source_field, mapping_type, target_field_id, target_field, action.id, value_mapping_field_id]

                # See if mappings have already a blocked mapping created
                blocked_field_ids = field_mapping_obj.search(cr, uid, [('blocked','=',True),('action_id','=',action.id)], context=context)
                blocked_field_ext_ids = field_mapping_obj.export_data(cr, uid, blocked_field_ids, ['id'])['datas']          
                if [vals[0]] in blocked_field_ext_ids:
                    continue
                mapping_data.append(vals)

            # load mapping
            mapping_fields = ['id', 'state','source_field_id/.id', 'source_field', 'type','target_field_id/.id', 'target_field','action_id/.id','value_mapping_field_id/.id']
            import_result = field_mapping_obj.load(cr, uid, mapping_fields, mapping_data)
            vals = {'log':import_result}
            if action_has_active_field == True:
                vals['source_domain'] = "['|',('active','=',False),('active','=',True)]"
                vals['repeating_action'] = repeating_action
            # write log and domain if active field exist
            self.write(cr, uid, [action.id], vals, context=context)
        # TODO, si algo anda lento o mal hay que borrar esto. No puedo hacer el check m2o depends ants de tenerlas ordenadas
        # return self.check_m2o_depends(cr, uid, ids, context=context)
        return True

    def check_m2o_depends(self, cr, uid, ids, context=None):
        ''' For action ids check if there are fields that should be load in a repeating action
        If there is at least one mapping field with repeating, make the action repeating '''
        field_mapping_obj = self.pool.get('etl.field_mapping')        

        for action in self.browse(cr, uid, ids):
            data = []
            repeating_action = False

            # Look for enabled or to analize future actions of this manager and this action
            future_action_ids = self.search(cr, uid, [('manager_id','=',action.manager_id.id),('sequence','>=',action.sequence),('state','in',['enabled','to_analyze'])], context=context)
            future_actions = []
            for future_action in self.browse(cr, uid, future_action_ids, context=context):
                future_actions.append(future_action.source_model_id.model)
            
            # Look for active fields of this action
            field_mapping_domain = [('blocked','!=',True),('action_id','=',action.id),('source_field_id.ttype','=', 'many2one'),('state','in',['enabled','to_analyze','on_repeating',]),('type','=','field')]
            field_mapping_ids = field_mapping_obj.search(cr, uid, field_mapping_domain, context=context)
            
            # If there are mappings with future dependencies make them 'on_repeating'
            for mapping in field_mapping_obj.browse(cr, uid, field_mapping_ids, context=context):
                dependency = mapping.source_field_id.relation
                if dependency in future_actions:
                    state = 'on_repeating'
                    repeating_action = True
                    vals = ['field_mapping_' + str(action.id) + '_' + str(mapping.source_field_id.id), state,]
                    data.append(vals) 
            fields = ['id', 'state']

            # if there is any repeating mapping field, then make action 'repeating action'
            import_result = field_mapping_obj.load(cr, uid, fields, data)
            vals = {
                'log':import_result,
                'repeating_action':repeating_action,
            }
            self.write(cr, uid, [action.id], vals, context=context)                       

    def updata_records_number(self, cr, uid, ids, source_connection=False, target_connection=False, context=None):
        migrator_model_obj = self.pool.get('etl.external_model')
        for action in self.browse(cr, uid, ids, context=context):
            if not source_connection or not target_connection:
                (source_connection, target_connection) = self.pool.get('etl.manager').open_connections(cr, uid, [action.manager_id.id], context=context)
                migrator_model_obj.get_records(cr, uid, [action.source_model_id.id], source_connection, context=context)
                migrator_model_obj.get_records(cr, uid, [action.target_model_id.id], target_connection, context=context)

    def run_repeated_action(self, cr, uid, ids, source_connection=False, target_connection=False, repeated_action=True, context=None):
        return self.run_action(cr, uid, ids, repeated_action=True, context=context)

    def run_action(self, cr, uid, ids, source_connection=False, target_connection=False, repeated_action=False, context=None):
        print 'Acciones que se van a correr: ', len(ids)
        migrator_model_obj = self.pool.get('etl.external_model')
        field_mapping_obj = self.pool.get('etl.field_mapping')
        value_mapping_field_detail_obj = self.pool.get('etl.value_mapping_field_detail')
        value_mapping_field_obj = self.pool.get('etl.value_mapping_field')
        for action in self.browse(cr, uid, ids, context=context):
            if not source_connection or not target_connection:
                (source_connection, target_connection) = self.pool.get('etl.manager').open_connections(cr, uid, [action.manager_id.id], context=context)
            print 'Running action external_model_id.type' + action.name
            domain = literal_eval(action.source_domain)
            if action.from_rec_id > 0:
                domain.append(('id','>=',action.from_rec_id))
            if action.to_rec_id > 0:
                domain.append(('id','<=',action.to_rec_id))

            source_model_obj = source_connection.get_model(action.source_model_id.model)
            target_model_obj = target_connection.get_model(action.target_model_id.model)

            source_model_ids = source_model_obj.search(domain)            
            print 'Records to import ', len(source_model_ids)
            print 'Building source data...'
            # Empezamos con  los campos que definimos como id
            source_fields = ['.id', action.source_id_exp]
            target_fields = [action.target_id_exp]

            if repeated_action:
                state = 'on_repeating'
            else:
                state = 'enabled'
            # source fields = enabled (or repeating) and type field
            source_fields.extend([x.source_field for x in action.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype != 'many2many'])

            # target fields = enabled and field then expression then migrated_id
            target_fields.extend([x.target_field for x in action.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype != 'many2many'])
            target_fields.extend([x.target_field for x in action.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype == 'many2many'])
            target_fields.extend([x.target_field for x in action.field_mapping_ids if x.state==state and x.type == 'value_mapping'])
            target_fields.extend([x.target_field for x in action.field_mapping_ids if x.state==state and x.type == 'date_adapt'])
            target_fields.extend([x.target_field for x in action.field_mapping_ids if x.state==state and x.type == 'expression'])
            target_fields.extend([x.target_field for x in action.field_mapping_ids if x.state==state and x.type == 'migrated_id'])
            
            # Read and append source values of type 'field' and type not m2m
            print 'Building none m2m field mapping...'
            source_model_data = source_model_obj.export_data(source_model_ids, source_fields)['datas']
            
            print 'Building m2m field mapping...'
            # Read and append source values of type 'field' and type m2m
            source_fields_m2m = [x.source_field for x in action.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype == 'many2many']
            for field in source_fields_m2m:
                for source_data_record in source_model_data:
                    source_data_m2m = source_model_obj.export_data([int(source_data_record[0])], ['.id', field])['datas']
                    for readed_record in source_data_m2m:
                        if readed_record[0]:
                            new_record = readed_record[1]
                        else:
                            new_record = new_record +','+ readed_record[1]
                    source_data_record.append(new_record)                
                source_data_m2m = source_model_obj.export_data(source_model_ids, ['id', field])['datas']

            print 'Building value mapping mapping...'
            # Read and append source values of type 'value_mapping'
            source_fields_value_mapping = [x.source_field for x in action.field_mapping_ids if x.state==state and x.type == 'value_mapping']
            source_data_value_mapping = source_model_obj.export_data(source_model_ids, source_fields_value_mapping)['datas']
            source_value_mapping_id = [x.value_mapping_field_id.id for x in action.field_mapping_ids if x.state==state and x.type == 'value_mapping']
            for readed_record, source_data_record in zip(source_data_value_mapping, source_model_data):
                target_record = []
                # print 'readed_record', readed_record
                # print 'source_data_record', source_data_record
                for field_value, value_mapping_id in zip(readed_record, source_value_mapping_id):
                    new_field_value = False
                    value_mapping = value_mapping_field_obj.browse(cr, uid,value_mapping_id, context=context)
                    # TODO mejorar esta cosa horrible, no hace falta guardar en dos clases separadas, deberia usar una sola para selection y para id
                    if value_mapping.type == 'id':
                        new_field_ids = value_mapping_field_detail_obj.search(cr, uid, [('source_external_model_record_id.ext_id','=',field_value),
                            ('value_mapping_field_id','=',value_mapping_id)], context=context)
                        if new_field_ids:
                            new_field_value = value_mapping_field_detail_obj.browse(cr, uid, new_field_ids[0], context=context).target_external_model_record_id.ext_id                    
                    elif value_mapping.type == 'selection':
                        new_field_ids = value_mapping_field_detail_obj.search(cr, uid, [('source_value_id.ext_id','=',field_value),
                            ('value_mapping_field_id','=',value_mapping_id)], context=context)
                        if new_field_ids:
                            new_field_value = value_mapping_field_detail_obj.browse(cr, uid, new_field_ids[0], context=context).target_value_id.ext_id                    
                    target_record.append(new_field_value)
                source_data_record.extend(target_record)

            print 'Building date adapt...'
            # Read and append source values of type 'date_adapt'
            source_fields_date_adapt = [x.source_field for x in action.field_mapping_ids if x.state==state and x.type == 'date_adapt']
            source_data_date_adapt = source_model_obj.export_data(source_model_ids, source_fields_date_adapt)['datas']
            source_mapping_date_adapt = [x for x in action.field_mapping_ids if x.state==state and x.type == 'date_adapt']
            for readed_record, source_data_record in zip(source_data_date_adapt, source_model_data):
                target_record = []
                for field_value, source_mapping in zip(readed_record, source_mapping_date_adapt):
                    if source_mapping.source_field_id.ttype == 'datetime' and field_value:
                        if source_mapping.target_field_id.ttype == 'date':
                            # TODO, no estoy seguro si esta forma de truncarlo funciona bien
                            field_value = field_value[:10]
                    if source_mapping.source_field_id.ttype == 'date' and field_value:
                        if source_mapping.target_field_id.ttype == 'datetime':
                            field_value = self.date_to_datetime(cr, uid, field_value, context=context)
                    target_record.append(field_value)
                source_data_record.extend(target_record)

            print 'Building expressions...'
            field_mapping_expression_ids = [x.id for x in action.field_mapping_ids if x.state==state and x.type == 'expression']
            if field_mapping_expression_ids:
                for rec in source_model_data:
                    rec_id = rec[0]
                    expression_results = field_mapping_obj.run_expressions(cr, uid, field_mapping_expression_ids, int(rec_id), source_connection, target_connection, context=context)
                    rec.extend(expression_results)
    
            print 'Building migrated ids...'
            field_mapping_migrated_id_ids = [x.id for x in action.field_mapping_ids if x.state==state and x.type == 'migrated_id']
            if field_mapping_migrated_id_ids:
                for rec in source_model_data:
                    rec_id = rec[0]
                    migrated_id_results = field_mapping_obj.get_migrated_id(cr, uid, field_mapping_migrated_id_ids, int(rec_id), source_connection, target_connection, context=context)
                    rec.extend(migrated_id_results)

            print 'Removing auxliaria .id...'
            target_model_data = []
            for record in source_model_data:
                target_model_data.append(record[1:])

            print 'Loading fields ...', target_fields
            # print 'data:', target_model_data
            try:
                import_result = target_model_obj.load(target_fields, target_model_data)
                vals = {'log':import_result}
            except:
                print 'error '
                error = sys.exc_info()
                vals = {'log':error}
            
            self.write(cr, uid, [action.id], vals, context=context)
            migrator_model_obj.get_records(cr, uid, [action.target_model_id.id], target_connection, context=context)            
        return True


    def order_actions(self, cr, uid, ids, exceptions=None, context=None):
        print ('Lines to order', len(ids))
        if exceptions == None:
            exceptions = []
        field_mapping_obj = self.pool.get('etl.field_mapping')   
        ordered_actions = []
        actions_to_order = []
        ordered_ids = []

        # We exclude de exceptions
        unordered_ids = self.search(cr, uid, [('id','in',ids),('source_model_id.model','not in',exceptions)], context=context)
        print 'Request IDS', ids
        print 'Request IDS without exceptions', unordered_ids

        for rec in self.browse(cr, uid, ids, context=context):
            actions_to_order.append(rec.source_model_id.model)
        print 'Actions_to_order', actions_to_order
        count = 0
        count_max = len(ids) * 2
        while unordered_ids and (count<count_max):
            count += 1
            rec = self.browse(cr, uid, unordered_ids[0], context=context)
            print ''
            print 'Unordered_ids', unordered_ids
            action_clean_dependecies = []
            many2one_field_ids = field_mapping_obj.search(cr, uid, [('action_id','=',rec.id),('source_field_id.ttype','=','many2one'),('state','in',['to_analyze','enabled','on_repeating'])], context=context)
            for mapping in field_mapping_obj.browse(cr, uid, many2one_field_ids, context=context):
                if (mapping.source_field_id.relation not in action_clean_dependecies) and (mapping.source_field_id.relation in actions_to_order):
                    if not(mapping.source_field_id.relation == rec.source_model_id.model):
                        action_clean_dependecies.append(mapping.source_field_id.relation)
                    # else:
                        # TODOOOOOOOOOOOOOOOOOOOOOO usar este dato para algo! para macar la clase por ejemplo
            print 'Modelo: ',rec.source_model_id.model, ', depenencias: ', action_clean_dependecies
            dependecies_ok = True
            for action_dependecy in action_clean_dependecies:
                if (action_dependecy not in ordered_actions) and (action_dependecy not in exceptions):
                    dependecies_ok = False
                    break
            unordered_ids.remove(rec.id)
            if dependecies_ok:
                print 'Dependency ok!'
                ordered_ids.append(rec.id)
                ordered_actions.append(rec.source_model_id.model)
            else:
                print 'Break, dependency false!'
                unordered_ids.append(rec.id)

        print ''
        print 'Unordered Models:', unordered_ids
        print 'New Order:', ordered_actions
        
        # Add sequence to exception actions
        sequence = 0
        for exception in exceptions:
            exception_action_ids = self.search(cr, uid, [('id','in',ids),('source_model_id.model','=',exception)], context=context)
            sequence += 10
            vals = {
                'sequence': sequence,
            }
            self.write(cr, uid, exception_action_ids, vals, context=context)

        # Add sequence to ordered actions
        sequence = 500
        for action_id in ordered_ids:
            sequence += 10
            vals = {
                'sequence': sequence,
            }
            self.write(cr, uid, [action_id], vals, context=context)
        return [unordered_ids, ordered_ids]

    def dummy_button(self, cr, uid, ids, context=None):
        print self.pool.get('product.product').fields_get(cr, uid)

    def date_to_datetime(self, cr, uid, userdate, context=None):
        """ Convert date values expressed in user's timezone to
        server-side UTC timestamp, assuming a default arbitrary
        time of 12:00 AM - because a time is needed.
    
        :param str userdate: date string in in user time zone
        :return: UTC datetime string for server-side use
        """
        # TODO: move to fields.datetime in server after 7.0
        user_date = datetime.strptime(userdate, DEFAULT_SERVER_DATE_FORMAT)
        if context and context.get('tz'):
            tz_name = context['tz']
        else:
            tz_name = self.pool.get('res.users').read(cr, SUPERUSER_ID, uid, ['tz'])['tz']
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            user_datetime = user_date + relativedetla(hours=12.0)
            local_timestamp = context_tz.localize(user_datetime, is_dst=False)
            user_datetime = local_timestamp.astimezone(utc)
            return user_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return user_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)   