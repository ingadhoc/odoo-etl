# -*- coding: utf-8 -*-
import openerplib
from openerp.tools.translate import _
from openerp.osv import fields, osv, orm
from ast import literal_eval

class manager(osv.osv):
    """"""
    
    _inherit = 'etl.manager'

    _columns = {
    }

    _defaults = {
        'model_exception_words': "['report','ir.logging','ir.qweb']",
        'model_disable_default': "['ir.model','ir.model.fields','ir.model.access','ir.model.data','ir.sequence.type','ir.sequence','ir.ui.menu','ir.ui.view.custom','ir.ui.view','ir.ui.view_sc','ir.default','ir.actions.actions','ir.actions.act_window','ir.actions.act_window.view','ir.actions.wizard','ir.actions.url','ir.server.object.lines','ir.actions.server','ir.actions.act_window_close','ir.actions.todo.category','ir.actions.todo','ir.actions.client','ir.values','ir.translation','ir.exports','ir.exports.line','workflow','workflow.activity','workflow.transition','workflow.instance','workflow.workitem','workflow.triggers','ir.rule','ir.module.category','ir.module.module','ir.module.module.dependency','res.widget','res.widget.user','publisher_warranty.contract','ir.module.record','board.board','board.board.line','decimal.precision','process.process','process.node','process.condition','process.transition','process.transition.action','email_template.preview','account.tax.template','account.account.template','account.tax.code.template','account.chart.template','account.fiscal.position.template','account.fiscal.position.tax.template','account.fiscal.position.account.template','temp.range','mrp.property.group','mrp.property','account.invoice.ar.installer','pos.config.journal','oo.config','mass.object','mass.editing.wizard','support.support_contract','support.email','account_analytic_analysis.summary.user','account_analytic_analysis.summary.month','res.groups','mail.alias']",
        'model_analyze_default': "['ir.attachment','ir.cron','ir.filters','ir.config_parameter','ir.mail_server','res.country','res.country.state','res.lang','res.currency','res.currency.rate.type','res.currency.rate','multi_company.default','res.company','res.users','res.request','res.request.link','res.request.history','res.log','ir.property','mail.message','mail.thread','product.uom.categ','product.uom','product.ul','product.price.type','product.pricelist.type','base.action.rule','email.template','fetchmail.server','edi.document','account.tax','account.account','account.journal.view','account.journal.column','account.fiscalyear','account.period','account.journal.period','account.analytic.journal','account.fiscal.position','account.fiscal.position.tax','account.fiscal.position.account','account.sequence.fiscalyear','procurement.order','sale.shop','document.storage','document.directory','document.directory.dctx','document.directory.content.type','document.directory.content','account.voucher',]",
        'field_disable_default': "['lang','printed_vat','context_lang','context_department_id','groups_id','alias_defaults','alias_id','alias_model_id','create_date','calendar_last_notif_ack',]",
        'field_analyze_default': "['reconcile_partial_id','reconcile_id']",
        'repeating_models': "['res.partner','res.company','res.users','account.fiscalyear','product.template','product.product','purchase.order','sale.order','hr.employee','project.task','procurement.order']",
        'field_disable_words': "['in_group','sel_groups_','rml_header','rml_foot',]",
    }

    def copy(self, cr, uid, id, default=None, context=None):
        if not context:
            context = {}
        default.update({
            'action_ids': False,
            'external_model_ids': False,
            'value_mapping_field_ids': False,
            })
        return super(manager, self).copy(cr, uid, id, default, context)      

    def open_connections(self, cr, uid, ids, context=None):
        '''Open connections for ids manager, only one manager should be passed'''
        # TODO return more than one connection or validate only one manager
        for manager in self.browse(cr, uid, ids):        
            source_hostname = manager.source_hostname
            source_port= manager.source_port
            source_database = manager.source_database
            source_login = manager.source_login
            source_password = manager.source_password
            try:
                source_connection = openerplib.get_connection(hostname=source_hostname, database=source_database, \
                    login=source_login, password=source_password, port=source_port)
            except:
                print 'error 111111111111'
            target_hostname = manager.target_hostname
            target_port= manager.target_port
            target_database = manager.target_database
            target_login = manager.target_login
            target_password = manager.target_password
            try:
                target_connection = openerplib.get_connection(hostname=target_hostname, database=target_database, \
                    login=target_login, password=target_password, port=target_port)
            except:
                print 'error 222222222222'            
        return [source_connection, target_connection]


    def delete_workflows(self, cr, uid, ids, context=None):
        for manager in self.browse(cr, uid, ids):
            (source_connection, target_connection) = self.open_connections(cr, uid, [manager.id], context=context)
            target_wf_instance_obj = target_connection.get_model("workflow.instance")
            res_types = literal_eval(manager.workflow_models)
            target_wf_instance_ids = target_wf_instance_obj.search([('res_type','in',res_types)])
            target_wf_instance_obj.unlink(target_wf_instance_ids)

    def install_modules(self, cr, uid, ids, context=None):
        for manager in self.browse(cr, uid, ids):
            (source_connection, target_connection) = self.open_connections(cr, uid, [manager.id], context=context)
            target_module_obj = target_connection.get_model("ir.module.module")
            modules = literal_eval(manager.modules_to_install)
            print 'modules', modules
            domain = [('name','in',modules)]
            target_module_ids = target_module_obj.search(domain)   
            print 'target_module_ids', target_module_ids
            target_module_obj.button_immediate_install(target_module_ids)

    def run_actions(self, cr, uid, ids, context=None):
        '''Run all actions (none repeating) of ids managers'''
        action_obj = self.pool.get('etl.action')
        for i in ids:
            (source_connection, target_connection) = self.open_connections(cr, uid, [i], context=context)
            action_ids = action_obj.search(cr, uid, [('manager_id','=',i),('state','=', 'enabled')], order='sequence', context=context)
            action_obj.run_action(cr, uid, action_ids, source_connection, target_connection, context=context)

    def run_repeated_actions(self, cr, uid, ids, context=None):
        '''Run all repeating actions of ids managers'''
        action_obj = self.pool.get('etl.action')
        for i in ids:
            (source_connection, target_connection) = self.open_connections(cr, uid, [i], context=context)      
            action_ids = action_obj.search(cr, uid, [('manager_id','=',i),('repeating_action','=',True),('state','=', 'enabled')], order='sequence', context=context)
            action_obj.run_repeated_action(cr, uid, action_ids, source_connection, target_connection, context=context)

    def match_models_and_order_actions(self, cr, uid, ids, context=None):    
        '''Match models and order the actions for ids managers''' 
        for manager in self.browse(cr, uid, ids):
            self.match_models(cr, uid, [manager.id], context=context)
            self.order_actions(cr, uid, [manager.id], context=context)
        return True
    
    def match_models(self, cr, uid, ids, context=None):
        '''Match models for ids managers'''
        etl_model_obj = self.pool.get('etl.external_model') 
        action_obj = self.pool.get('etl.action') 
        for manager in self.browse(cr, uid, ids):
            print 'Matching models for manager ', manager.name
            # read all source models
            source_domain = [('manager_id','=',manager.id),('type','=','source')]
            source_model_ids = etl_model_obj.search(cr, uid, source_domain, context=context)

            # get disable and to analyze models
            data = []
            model_disable_default = []
            model_analyze_default = []
            if manager.model_disable_default:
                model_disable_default = literal_eval(manager.model_disable_default)
            if manager.model_analyze_default:
                model_analyze_default = literal_eval(manager.model_analyze_default)

            # get blocked external ids models
            blocked_model_ids = action_obj.search(cr, uid, [('blocked','=',True),('manager_id','=',manager.id)], context=context)
            blocked_model_ext_ids = action_obj.export_data(cr, uid, blocked_model_ids, ['id'])['datas']          
            
            # for each source model look for a target model and give state
            for model in etl_model_obj.browse(cr, uid, source_model_ids, context=context):
                target_model_id = False
                target_domain = [('manager_id','=',manager.id),('type','=','target'),('model','=',model.model)]
                target_model_ids = etl_model_obj.search(cr, uid, target_domain, context=context)

                if target_model_ids:
                    target_model_id = target_model_ids[0]

                # give right state to model mapping 
                state = 'enabled'
                if model.model in model_disable_default:
                    state = 'disabled'
                elif model.model in model_analyze_default or not target_model_id:
                    state = 'to_analyze'
                if model.records == 0:
                    state = 'no_records'

                # get vals for action mapping and create and id
                vals = ['model_mapping_' + str(manager.id) + '_' + str(model.id), 
                    state, 
                    model.name + ' (' + model.model + ')', 
                    model.order, 
                    model.id, 
                    target_model_id, 
                    manager.id]

                # look if this id should be blocked
                if [vals[0]] in blocked_model_ext_ids:
                    continue

                # append if not to data
                data.append(vals)

            # write actions with data an fields, give result to log
            action_fields = ['id', 'state', 'name', 'sequence', 'source_model_id/.id', 
                'target_model_id/.id','manager_id/.id']
            print 'Loading actions match for manager ', manager.name
            import_result = action_obj.load(cr, uid, action_fields, data)
            vals = {
                'log':import_result
            }

            # write log on manager
            self.write(cr, uid, [manager.id], vals, context=context)
            
            # call for match fields
            print 'Matching fields for for manager ', manager.name
            action_obj.match_fields(cr, uid, import_result['ids'], context=context)
        return True

    def order_actions(self, cr, uid, ids, context=None):     
        '''Order actions for ids managers'''
        action_obj = self.pool.get('etl.action')
        for manager in self.browse(cr, uid, ids):
            # Get enabled actions
            action_ids = action_obj.search(cr, uid, [('manager_id','=',manager.id),('state','in',['to_analyze','enabled'])], context=context)
            
            # If repeating_mdodels defined on the manager, take them as exceptions
            exceptions = []
            if manager.repeating_models:
                repeating_models = manager.repeating_models
                exceptions = literal_eval(repeating_models)            
            
            # Get unordered and ordered ids from action model
            (unordered_ids, ordered_ids) = action_obj.order_actions(cr, uid, action_ids, exceptions, context=context)

            # get unordered and ordered actions names to write in log. Write log
            ordered_actions = []
            unordered_actions = []
            for ordered_action in action_obj.browse(cr, uid, ordered_ids, context=context):
                ordered_actions.append(ordered_action.source_model_id.model)
            for unordered_action in action_obj.browse(cr, uid, unordered_ids, context=context):
                unordered_actions.append(unordered_action.source_model_id.model)    
            vals = {
                'log': 'Ordered actions: ' + str(ordered_actions) + '\n' + '\n' + 'Unordered actions: ' + str(unordered_actions)
            }            
            self.write(cr, uid, [manager.id], vals, context=context)

            # check actions depends if no unordered_ids
            if not unordered_ids:
                action_obj.check_m2o_depends(cr, uid, action_ids, context=context)
        return True  

    def read_and_get(self, cr, uid, ids, context=None):
        '''Read source and target models and get records number'''
        for manager in self.browse(cr, uid, ids):
            (source_connection, target_connection) = self.open_connections(cr, uid, [manager.id], context=context)
            self.read_models(cr, uid, [manager.id], context=context)
            self.get_records(cr, uid, [manager.id], context=context)
        return True

    def get_records(self, cr, uid, ids, context=None):    
        '''Get number of records for source and target models of manager ids'''
        etl_model_obj = self.pool.get('etl.external_model')
        for manager in self.browse(cr, uid, ids):
            (source_connection, target_connection) = self.open_connections(cr, uid, [manager.id], context=context)
            source_model_ids = etl_model_obj.search(cr, uid, [('type','=','source'),('manager_id','=',manager.id)], context=context)
            target_model_ids = etl_model_obj.search(cr, uid, [('type','=','target'),('manager_id','=',manager.id)], context=context)
            etl_model_obj.get_records(cr, uid, source_model_ids, source_connection, context=context)
            etl_model_obj.get_records(cr, uid, target_model_ids, target_connection, context=context)
        return True 

    def read_models(self, cr, uid, ids, context=None):  
        '''Get models and fields of source and target database for manager ids'''
        external_model_obj = self.pool['etl.external_model']
        for manager in self.browse(cr, uid, ids):
            (source_connection, target_connection) = self.open_connections(cr, uid, [manager.id], context=context)
            self.read_model(cr, uid, source_connection, 'source', manager.id, context=context)
            self.read_model(cr, uid, target_connection, 'target', manager.id, context=context)
            source_external_model_ids = external_model_obj.search(cr, uid, [('manager_id','=', manager.id),('type','=','source')], context=context)
            target_external_model_ids = external_model_obj.search(cr, uid, [('manager_id','=', manager.id),('type','=','target')], context=context)
            external_model_obj.read_fields(cr, uid, source_external_model_ids, source_connection, context=context)
            external_model_obj.read_fields(cr, uid, target_external_model_ids, target_connection, context=context)
        return True                 

    def read_model(self, cr, uid, connection, relation_type, manager_id, context=None):     
        ''' Get models for one manger and one type (source or target)'''
        external_model_obj = connection.get_model("ir.model")
        etl_model_obj = self.pool.get('etl.external_model')

        # osv_memory = False for not catching transients models
        domain = [('osv_memory','=',False)]
        
        # catch de models excpections worlds and append to search domain
        words_exception = self.browse(cr, uid, manager_id, context=context).model_exception_words
        if words_exception:
            words_exception = literal_eval(words_exception)
            for exception in words_exception:
                domain.append(('model', 'not like', exception))

        # get external model ids
        external_model_ids = external_model_obj.search(domain)      
          
        # read id, model and name of external models
        external_model_fields = ['.id', 'model', 'name']
        export_data = external_model_obj.export_data(external_model_ids, external_model_fields)          
        
        # We fix .id to id because we are going to use it
        external_model_fields[0] = 'id'

        # We add the type, manager and sequence to external fields and to data
        external_model_fields.extend(['type', 'manager_id/.id', 'sequence'])
        external_model_data = []
        for record in export_data['datas']:
            # we extend each record with type, manager and a sequence
            record.extend([relation_type, manager_id, int(record[0]) * 10])
            # replace the .id with our own external identifier
            record [0] = 'man_' + str(manager_id) + '_' + relation_type + '_' + str(record[1]).replace('.','_')
            # record [0] = 'man_' + str(manager_id) + '_' + relation_type + '_model_' + str(record[0])
            external_model_data.append(record)
        
        # Load external_model_data to external models model
        rec_ids = etl_model_obj.load(cr, uid, external_model_fields, external_model_data, context=None)        
        return rec_ids  