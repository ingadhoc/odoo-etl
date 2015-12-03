# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from erppeek import Client
from ast import literal_eval
import logging
_logger = logging.getLogger(__name__)


class manager(models.Model):
    """"""

    _name = 'etl.manager'
    _description = 'manager'

    name = fields.Char(
        string='Name',
        required=True
        )
    source_hostname = fields.Char(
        string='Source Hostname',
        required=True,
        default='http://localhost',
        )
    source_port = fields.Integer(
        string='Source Port',
        required=True
        )
    source_database = fields.Char(
        string='Source Database',
        required=True
        )
    source_login = fields.Char(
        string='Source Login',
        required=True
        )
    source_password = fields.Char(
        string='Source Password',
        required=True
        )
    target_hostname = fields.Char(
        string='Target Hostname',
        required=True,
        default='http://localhost',
        )
    target_port = fields.Integer(
        string='Target Port',
        required=True
        )
    target_database = fields.Char(
        string='Target Database',
        required=True
        )
    target_login = fields.Char(
        string='Target Login',
        required=True
        )
    target_password = fields.Char(
        string='Target Password',
        required=True
        )
    log = fields.Text(
        string='Log'
        )
    model_disable_default = fields.Text(
        string='Models Disabled by Default',
        # TODO move this default to another model
        default="['ir.model','ir.model.fields','ir.model.access','ir.model.data','ir.sequence.type','ir.sequence','ir.ui.menu','ir.ui.view.custom','ir.ui.view','ir.ui.view_sc','ir.default','ir.actions.actions','ir.actions.act_window','ir.actions.act_window.view','ir.actions.wizard','ir.actions.url','ir.server.object.lines','ir.actions.server','ir.actions.act_window_close','ir.actions.todo.category','ir.actions.todo','ir.actions.client','ir.values','ir.translation','ir.exports','ir.exports.line','workflow','workflow.activity','workflow.transition','workflow.instance','workflow.workitem','workflow.triggers','ir.rule','ir.module.category','ir.module.module','ir.module.module.dependency','res.widget','res.widget.user','publisher_warranty.contract','ir.module.record','board.board','board.board.line','decimal.precision','process.process','process.node','process.condition','process.transition','process.transition.action','email_template.preview','account.tax.template','account.account.template','account.tax.code.template','account.chart.template','account.fiscal.position.template','account.fiscal.position.tax.template','account.fiscal.position.account.template','temp.range','mrp.property.group','mrp.property','account.invoice.ar.installer','pos.config.journal','oo.config','mass.object','mass.editing.wizard','support.support_contract','support.email','account_analytic_analysis.summary.user','account_analytic_analysis.summary.month','res.groups','mail.alias']"
        )
    field_disable_default = fields.Text(
        string='Fields Disable by Default',
        # TODO move this default to another model
        default="['lang','printed_vat','context_lang','context_department_id','groups_id','alias_defaults','alias_id','alias_model_id','create_date','calendar_last_notif_ack',]",
        )
    model_exception_words = fields.Char(
        string='Model Exception Words',
        # TODO move this default to another model
        default="['report','ir.logging','ir.qweb']",
        )
    model_analyze_default = fields.Text(
        string='Models Analyze by Default',
        # TODO move this default to another model
        default="['ir.attachment','ir.cron','ir.filters','ir.config_parameter','ir.mail_server','res.country','res.country.state','res.lang','res.currency','res.currency.rate.type','res.currency.rate','multi_company.default','res.company','res.users','res.request','res.request.link','res.request.history','res.log','ir.property','mail.message','mail.thread','product.uom.categ','product.uom','product.ul','product.price.type','product.pricelist.type','base.action.rule','email.template','fetchmail.server','edi.document','account.tax','account.account','account.journal.view','account.journal.column','account.fiscalyear','account.period','account.journal.period','account.analytic.journal','account.fiscal.position','account.fiscal.position.tax','account.fiscal.position.account','account.sequence.fiscalyear','procurement.order','sale.shop','document.storage','document.directory','document.directory.dctx','document.directory.content.type','document.directory.content','account.voucher',]",
        )
    note = fields.Html(
        string='Notes'
        )
    field_analyze_default = fields.Text(
        string='Fields Analize by Default',
        # TODO move this default to another model
        default="['reconcile_partial_id','reconcile_id']",
        )
    repeating_models = fields.Text(
        string='Repeating Models',
        # TODO move this default to another model
        default="['res.partner','res.company','res.users','account.fiscalyear','product.template','product.product','purchase.order','sale.order','hr.employee','project.task','procurement.order']",
        )
    field_disable_words = fields.Text(
        string='Fields Disable by Default Words',
        # TODO move this default to another model
        default="['in_group','sel_groups_','rml_header','rml_foot',]",
        )
    modules_to_install = fields.Text(
        string='Modules To Install',
        default=[]
        )
    workflow_models = fields.Char(
        string='Models to delete Workflows',
        required=True,
        default='[]'
        )
    action_ids = fields.One2many(
        'etl.action',
        'manager_id',
        string='Actions',
        domain=[('state', 'in', ['to_analyze', 'enabled'])],
        copy=False,
        )
    external_model_ids = fields.One2many(
        'etl.external_model',
        'manager_id',
        string='External Models',
        readonly=True,
        copy=False,
        )
    value_mapping_field_ids = fields.One2many(
        'etl.value_mapping_field',
        'manager_id',
        string='Value Mapping Fields',
        copy=False,
        )
    source_lang = fields.Char(
        'Source Language',
        required=True,
        default='en_US',
        # TODO improove this and load all translations for tranlatable fields
        help='Language used on source database translatable fields'
        )
    target_lang = fields.Char(
        'Target Language',
        required=True,
        default='en_US',
        # TODO improove this and load all translations for tranlatable fields
        help='Language used on target database translatable fields'
        )
    target_id_type = fields.Selection(
        [(u'source_id', 'Source ID'), (u'builded_id', 'Builded ID')],
        string='Target ID Type',
        required=True,
        default='builded_id',
        help="Selection on how the Records target ID's will be build:\n\t"
             "    - Source ID - will keep the source ID (external_id)\n\t"
             "    - Builded ID - every external ID will be build as concatenation of Manager Name + _ + Source Model"   
        )

    _constraints = [
    ]

    @api.multi
    def open_connections(self):
        '''
        '''
        self.ensure_one()
        try:
            _logger.info('Getting source connection')
            source_connection = Client(
                '%s:%i' % (self.source_hostname, self.source_port),
                db=self.source_database,
                user=self.source_login,
                password=self.source_password)
        except Exception, e:
            raise Warning(
                _("Unable to Connect to Database. 'Error: %s'") % e)
        try:
            _logger.info('Getting target connection')
            target_connection = Client(
                '%s:%i' % (self.target_hostname, self.target_port),
                db=self.target_database,
                user=self.target_login,
                password=self.target_password)
        except Exception, e:
            raise Warning(
                _("Unable to Connect to Database. 'Error: %s'") % e)
        return [source_connection, target_connection]

    @api.one
    def read_active_source_models(self):
        '''
        '''
        (source_connection, target_connection) = self.open_connections()
        actions = self.env['etl.action'].search(
            [('manager_id', '=', self.id), ('state', '=', 'enabled')],
            order='sequence')
        actions.read_source_model(source_connection, target_connection)

    @api.one
    def delete_workflows(self):
        (source_connection, target_connection) = self.open_connections()
        target_wf_instance_obj = target_connection.model("workflow.instance")
        res_types = literal_eval(self.workflow_models)
        target_wf_instance_ids = target_wf_instance_obj.search(
            [('res_type', 'in', res_types)])
        target_wf_instance_obj.unlink(target_wf_instance_ids)

    @api.one
    def install_modules(self):
        (source_connection, target_connection) = self.open_connections()
        target_module_obj = target_connection.model("ir.module.module")
        modules = literal_eval(self.modules_to_install)
        domain = [('name', 'in', modules)]
        target_module_ids = target_module_obj.search(domain)
        target_module_obj.button_immediate_install(target_module_ids)

    @api.one
    def run_actions(self):
        '''Run all actions (none repeating)'''
        (source_connection, target_connection) = self.open_connections()
        actions = self.env['etl.action'].search(
            [('manager_id', '=', self.id), ('state', '=', 'enabled')],
            order='sequence')
        actions.run_action(source_connection, target_connection)

    @api.one
    def run_repeated_actions(self):
        '''Run all repeating actions'''
        (source_connection, target_connection) = self.open_connections()
        actions = self.env['etl.action'].search([
            ('manager_id', '=', self.id),
            ('repeating_action', '=', True),
            ('state', '=', 'enabled')],
            order='sequence')
        actions.run_repeated_action(source_connection, target_connection)

    @api.one
    def match_models_and_order_actions(self):
        '''Match models and order the actions'''
        self.match_models()
        self.order_actions()
        return True

    @api.one
    def match_models(self):
        '''Match models'''
        _logger.info('Matching models for manager %s' % self.name)
        # read all source models
        source_domain = [('manager_id', '=', self.id), ('type', '=', 'source')]
        source_models = self.env['etl.external_model'].search(source_domain)

        # get disable and to analyze models
        data = []
        model_disable_default = []
        model_analyze_default = []
        if self.model_disable_default:
            model_disable_default = literal_eval(self.model_disable_default)
        if self.model_analyze_default:
            model_analyze_default = literal_eval(self.model_analyze_default)

        # get blocked external ids models
        blocked_models = self.env['etl.action'].search(
            [('blocked', '=', True), ('manager_id', '=', self.id)])
        blocked_model_ext_ids = blocked_models.export_data(['id'])['datas']

        # for each source model look for a target model and give state
        for model in source_models:
            target_domain = [
                ('manager_id', '=', self.id),
                ('type', '=', 'target'), ('model', '=', model.model)]
            target_model = self.env['etl.external_model'].search(
                target_domain, limit=1)

            # give right state to model mapping
            state = 'enabled'
            if model.model in model_disable_default:
                state = 'disabled'
            elif model.model in model_analyze_default or not target_model:
                state = 'to_analyze'
            if model.records == 0:
                state = 'no_records'

            # get vals for action mapping and create and id
            vals = [
                'model_mapping_' + str(self.id) + '_' + str(model.id),
                state,
                model.name + ' (' + model.model + ')',
                model.order,
                model.id,
                target_model and target_model.id or False,
                self.id
                ]

            # look if this id should be blocked
            if [vals[0]] in blocked_model_ext_ids:
                continue

            # append if not to data
            data.append(vals)

        # write actions with data an fields, give result to log
        action_fields = [
            'id', 'state', 'name', 'sequence', 'source_model_id/.id',
            'target_model_id/.id', 'manager_id/.id'
            ]
        _logger.info('Loading actions match for manager %s' % self.name)
        import_result = self.env['etl.action'].load(action_fields, data)

        # write log on manager
        self.log = import_result

        # call for match fields
        _logger.info('Matching fields for models %s of manager %s' % (
            import_result['ids'], self.name))
        self.env['etl.action'].browse(import_result['ids']).match_fields()

    @api.one
    def order_actions(self):
        '''Order actions for ids managers'''
        # Get enabled actions
        actions = self.env['etl.action'].search([
            ('manager_id', '=', self.id),
            ('state', 'in', ['to_analyze', 'enabled'])])

        # If repeating_mdodels defined on the manager, take them as exceptions
        exceptions = []
        if self.repeating_models:
            repeating_models = self.repeating_models
            exceptions = literal_eval(repeating_models)

        # Get unordered and ordered ids from action model
        (unordered_ids, ordered_ids) = actions.order_actions(exceptions)

        # get unordered and ordered actions names to write in log. Write log
        ordered_actions = []
        unordered_actions = []
        for ordered_action in self.env['etl.action'].browse(ordered_ids):
            ordered_actions.append(ordered_action.source_model_id.model)
        for unordered_action in self.env['etl.action'].browse(unordered_ids):
            unordered_actions.append(unordered_action.source_model_id.model)
        self.log = 'Ordered actions: %s\n\nUnordered actions: %s' % (
            str(ordered_actions), str(unordered_actions))

        # check actions depends if no unordered_ids
        if not unordered_ids:
            actions.check_m2o_depends()

    @api.one
    def read_and_get(self):
        '''Read source and target models and get records number'''
        (source_connection, target_connection) = self.open_connections()
        self.read_models()
        self.get_records()

    @api.one
    def get_records(self):
        '''Get number of records for source and target models'''
        (source_connection, target_connection) = self.open_connections()
        source_models = self.env['etl.external_model'].search(
            [('type', '=', 'source'), ('manager_id', '=', self.id)])
        target_models = self.env['etl.external_model'].search(
            [('type', '=', 'target'), ('manager_id', '=', self.id)])
        source_models.get_records(source_connection)
        target_models.get_records(target_connection)

    @api.one
    def read_models(self):
        '''Get models and fields of source and target database'''
        # external_model_obj = self.pool['etl.external_model']
        (source_connection, target_connection) = self.open_connections()
        self.read_model(source_connection, 'source')[self.id]
        self.read_model(target_connection, 'target')[self.id]
        source_external_models = self.env['etl.external_model'].search([
            ('manager_id', '=', self.id), ('type', '=', 'source')])
        target_external_models = self.env['etl.external_model'].search([
            ('manager_id', '=', self.id), ('type', '=', 'target')])
        source_external_models.read_fields(source_connection)
        target_external_models.read_fields(target_connection)

    @api.multi
    def read_model(self, connection, relation_type):
        ''' Get models for one manger and one type (source or target)'''
        res = {}
        for manager in self:
            external_model_obj = connection.model("ir.model")

            # osv_memory = False for not catching transients models
            domain = [('osv_memory', '=', False)]

            # catch de models excpections worlds and append to search domain
            words_exception = manager.model_exception_words
            if words_exception:
                words_exception = literal_eval(words_exception)
                for exception in words_exception:
                    domain.append(('model', 'not like', exception))

            # get external model ids
            external_model_ids = external_model_obj.search(domain)

            # read id, model and name of external models
            external_model_fields = ['.id', 'model', 'name']
            export_data = external_model_obj.export_data(
                external_model_ids, external_model_fields)

            # We fix .id to id because we are going to use it
            external_model_fields[0] = 'id'

            # We add the type, manager and sequence to external fields and data
            external_model_fields.extend(
                ['type', 'manager_id/.id', 'sequence'])
            external_model_data = []
            for record in export_data['datas']:
                # we extend each record with type, manager and a sequence
                record.extend([relation_type, manager.id, int(record[0]) * 10])
                # replace the .id with our own external identifier
                record[0] = 'man_%s_%s_%s' % (
                    str(manager.id),
                    relation_type,
                    str(record[1]).replace('.', '_')
                    )
                external_model_data.append(record)

            # Load external_model_data to external models model
            rec_ids = self.env['etl.external_model'].load(
                external_model_fields, external_model_data)
            res[manager.id] = rec_ids
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
