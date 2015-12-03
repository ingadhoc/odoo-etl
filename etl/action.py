# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, SUPERUSER_ID
import sys
import pytz
from ast import literal_eval
from datetime import datetime
from dateutil import relativedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import logging
_logger = logging.getLogger(__name__)


class action(models.Model):
    """"""

    _name = 'etl.action'
    _description = 'action'

    _order = "sequence"

    blocked = fields.Boolean(
        string='Blocked',
        copy=False,
        )
    sequence = fields.Integer(
        string='Sequence'
        )
    state = fields.Selection(
        [(u'to_analyze', 'to_analyze'), (u'enabled', 'enabled'), (u'disabled', 'disabled'), (u'no_records', 'no_records')],
        string='State',
        required=True
        )
    name = fields.Char(
        string='Name',
        required=True
        )
    source_domain = fields.Char(
        string='Source Domain',
        required=True,
        default='[]'
        )
    log = fields.Text(
        string='Log'
        )
    note = fields.Html(
        string='Notes'
        )
    repeating_action = fields.Boolean(
        string='Repeating Action?',
        store=True,
        compute='_get_repeating_action',
        )
    source_id_exp = fields.Char(
        string='source_id_exp',
        required=True,
        default='id'
        )
    target_id_type = fields.Selection(
        [(u'source_id', 'source_id'), (u'builded_id', 'builded_id')],
        string='Target ID Type',
        required=True,
        related='manager_id.target_id_type'
        )
    from_rec_id = fields.Integer(
        string='From Record'
        )
    to_rec_id = fields.Integer(
        string='To Record'
        )
    target_id_prefix = fields.Char(
        string='target_id_prefix',
        compute='_get_action_prefix'
        )
    manager_id = fields.Many2one(
        'etl.manager',
        ondelete='cascade',
        string='Manager',
        required=True
        )
    field_mapping_ids = fields.One2many(
        'etl.field_mapping',
        'action_id',
        string='Fields Mapping',
        copy=False,
        )
    source_model_id = fields.Many2one(
        'etl.external_model',
        string='Source Model',
        required=True,
        ondelete='cascade',
        )
    target_model_id = fields.Many2one(
        'etl.external_model',
        string='Target Model',
        ondelete='cascade',
        )
    source_records = fields.Integer(
        related='source_model_id.records',
        readonly=True,
        string='Source Records',
        )
    target_records = fields.Integer(
        related='target_model_id.records',
        readonly=True,
        string='Target Records',
        )

    _constraints = [
    ]

    @api.one
    @api.depends(
        'source_model_id.model','target_id_type'
        )
    def _get_action_prefix(self):
        value = False
        if self.target_id_type == 'builded_id':
             value = self.manager_id.name + '_' + self.source_model_id.model.replace('.','_')
        self.target_id_prefix = value             

    @api.one
    @api.depends(
        'field_mapping_ids.state'
        )
    def _get_repeating_action(self):
        repeating_action = False
        repeating_field_mapps = self.field_mapping_ids.search([
            ('state', '=', 'on_repeating'),
            ('action_id', '=', self.id),
            ])
        if repeating_field_mapps:
            repeating_action = True
        self.repeating_action = repeating_action
        
    @api.multi
    def action_block(self):
        return self.write({'blocked': True})

    @api.one
    def match_fields(self):
        ''' Match fields'''
        _logger.info("Matching fields on action %s" % self.name)
        migrator_field = self.env['etl.field']
        field_mapping = self.env['etl.field_mapping']

        # Get disabled and to analize words and fields
        field_disable_default = []
        field_analyze_default = []
        field_disable_words = []
        if self.manager_id.field_disable_default:
            field_disable_default = literal_eval(
                self.manager_id.field_disable_default)
        if self.manager_id.field_analyze_default:
            field_analyze_default = literal_eval(
                self.manager_id.field_analyze_default)
        if self.manager_id.field_disable_words:
            field_disable_words = literal_eval(
                self.manager_id.field_disable_words)

        # get source fields thar are not functions ore one2many
        # Function in False or in '_fnct_read' (aparentemente _fnct_read es para campos related y los queremos mapear)
        source_domain = [
            ('model_id.id', '=', self.source_model_id.id),
            ('ttype', 'not in', ['one2many']),
            '|', ('function', 'in', [False, '_fnct_read']),
            ('required', '=', 'True')]
        source_fields = migrator_field.search(source_domain)

        mapping_data = []
        action_has_active_field = False
        for field in source_fields:
            # If nothing asserts, choose expresion
            mapping_type = 'expression'

            # build source_field with or not /id
            source_field_name = field.name
            if field.ttype in ['many2one', 'many2many']:
                source_field_name += '/id'

            # look for a target field
            target_domain = [
                ('model_id.id', '=', self.target_model_id.id),
                ('name', '=', field.name)]
            target_fields = migrator_field.search(target_domain)

            # check the state
            state = 'enabled'
            if field.name in field_analyze_default or not target_fields:
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
            target_field_name = False
            if target_fields:
                mapping_type = 'field'
                target_field = target_fields[0]

                target_field_name = target_field.name
                if target_field.ttype in ['many2one', 'many2many']:
                    target_field_name += '/id'
                    if target_field.ttype == 'many2many':
                        relation = target_field.relation
                        previus_actions = self.search([
                            ('manager_id', '=', self.manager_id.id),
                            ('sequence', '<', self.sequence),
                            ('target_model_id.model', '=', relation)])
                        if not previus_actions:
                            state = 'other_class'
                elif field.ttype == 'datetime' and target_field.ttype == 'date' or field.ttype == 'date' and target_field.ttype == 'datetime':
                    mapping_type = 'date_adapt'
                elif field.ttype == 'reference':
                    mapping_type = 'reference'

            # Check if there is any value mapping for current field
            value_mapping_field = False
            value_mappings = self.env['etl.value_mapping_field'].search([
                ('source_model_id.model', '=', field.relation),
                ('manager_id', '=', self.manager_id.id)])
            if value_mappings:
                mapping_type = 'value_mapping'
                value_mapping_field = value_mappings[0]

            # If field name = 'state' then we upload it on a repeating action so we are sure we can upload all the related data
            if field.name == 'state':
                state = 'on_repeating'
            vals = [
                'field_mapping_' + str(self.id) + '_' + str(field.id),
                state,
                field.id,
                source_field_name,
                mapping_type,
                target_field and target_field.id or False,
                target_field_name,
                self.id,
                value_mapping_field and value_mapping_field.id or False]

            # See if mappings have already a blocked mapping created
            blocked_fields = field_mapping.search([
                ('blocked', '=', True),
                ('action_id', '=', self.id)])
            blocked_field_ext_ids = blocked_fields.export_data(
                ['id'])['datas']
            if [vals[0]] in blocked_field_ext_ids:
                continue
            mapping_data.append(vals)

        # load mapping
        mapping_fields = [
            'id',
            'state',
            'source_field_id/.id',
            'source_field',
            'type',
            'target_field_id/.id',
            'target_field',
            'action_id/.id',
            'value_mapping_field_id/.id']
        _logger.info("Loading mapping fields for action %s" % self.name)
        import_result = field_mapping.load(mapping_fields, mapping_data)
        vals = {'log': import_result}

        if action_has_active_field and self.source_domain == '[]':
            vals['source_domain'] = "['|',('active','=',False),('active','=',True)]"
        # write log and domain if active field exist
        self.write(vals)
        # TODO, si algo anda lento o mal hay que borrar esto. No puedo hacer el check m2o depends ants de tenerlas ordenadas
        # return self.check_m2o_depends(cr, uid, ids, context=context)
        # return True

    @api.one
    def check_m2o_depends(self):
        ''' Check if there are fields that should be load in a repeating action
        If there is at least one mapping field with repeating,
        make the action repeating '''
        data = []

        # Look for enabled or to analize future actions of this manager and
        # this action
        future_actions = self.search([
            ('manager_id', '=', self.manager_id.id),
            ('sequence', '>=', self.sequence),
            ('state', 'in', ['enabled', 'to_analyze'])])
        future_models = []
        for future_action in future_actions:
            future_models.append(future_action.source_model_id.model)

        # Look for active fields of this action
        field_mapping_domain = [
            ('blocked', '!=', True),
            ('action_id', '=', self.id),
            ('source_field_id.ttype', '=', 'many2one'),
            ('state', 'in', ['enabled', 'to_analyze', 'on_repeating']),
            ('type', '=', 'field')]
        field_mappings = self.env['etl.field_mapping'].search(
            field_mapping_domain)

        # If there are mappings with future depends make them 'on_repeating'
        for mapping in field_mappings:
            dependency = mapping.source_field_id.relation
            if dependency in future_models:
                state = 'on_repeating'
                vals = [
                    'field_mapping_%s_%s' % (
                        str(self.id),
                        str(mapping.source_field_id.id)),
                    state]
                data.append(vals)
        fields = ['id', 'state']

        # if there is any repeating mapping field, then make action
        # 'repeating action'
        import_result = self.env['etl.field_mapping'].load(fields, data)
        vals = {
            'log': import_result,
        }
        self.write(vals)

    @api.one
    def updata_records_number(
            self, source_connection=False, target_connection=False):
        if not source_connection or not target_connection:
            (source_connection, target_connection) = self.manager_id.open_connections()
        self.source_model_id.get_records(source_connection)
        self.target_model_id.get_records(target_connection)

    @api.multi
    def run_repeated_action(
            self, source_connection=False, target_connection=False,
            repeated_action=True):
        return self.run_action(repeated_action=True)

    @api.multi
    def read_source_model(
            self, source_connection=False, target_connection=False,
            repeated_action=False, context=None):
        readed_model = []
        for action in self:
            if action.source_model_id.id in readed_model:
                continue
            _logger.info('Reading model %s' % action.source_model_id.model)
            if not source_connection:
                (source_connection, target_connection) = action.manager_id.open_connections()
            source_model_obj = source_connection.model(action.source_model_id.model)
            domain = []
            active_field = action.env['etl.field'].search([
                ('model_id', '=', action.source_model_id.id),
                ('name', '=', 'active'),
                ], limit=1)
            if active_field:
                domain = [('active', 'in', [True, False])]
            source_model_ids = source_model_obj.search(domain)
            source_model_obj.export_data(source_model_ids, ['id'])
            readed_model.append(action.source_model_id.id)

    @api.one
    def run_action(
            self, source_connection=False, target_connection=False,
            repeated_action=False):
        _logger.info('Actions to run: %i' % len(self.ids))
        action_obj = self.env['etl.action']
        model_obj = self.env['etl.external_model']
        field_mapping_obj = self.env['etl.field_mapping']
        value_mapping_field_detail_obj = self.env['etl.value_mapping_field_detail']
        value_mapping_field_obj = self.env['etl.value_mapping_field']
        if not source_connection or not target_connection:
            (source_connection, target_connection) = self.manager_id.open_connections()
        # add language to connections context
        source_connection.context = {'lang': self.manager_id.source_lang}
        target_connection.context = {'lang': self.manager_id.target_lang}
        _logger.info('Running action external_model_id.type %s' % self.name)

        domain = literal_eval(self.source_domain)
        if self.from_rec_id > 0:
            domain.append(('id', '>=', self.from_rec_id))
        if self.to_rec_id > 0:
            domain.append(('id', '<=', self.to_rec_id))

        source_model_obj = source_connection.model(self.source_model_id.model)
        target_model_obj = target_connection.model(self.target_model_id.model)

        source_model_ids = source_model_obj.search(domain)
        _logger.info('Records to import %i' % len(source_model_ids))

        _logger.info('Building source data...')
        # Empezamos con  los campos que definimos como id
        source_fields = ['.id', self.source_id_exp]
        target_fields = ['id']

        if repeated_action:
            state = 'on_repeating'
        else:
            state = 'enabled'

        # source fields = enabled (or repeating) and type field
        source_fields.extend([x.source_field for x in self.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype != 'many2many' and x.source_field_id.ttype != 'many2one'])
        #print source_fields
        # target fields = enabled and field then expression then migrated_id
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype != 'many2many' and x.source_field_id.ttype != 'many2one'])
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype == 'many2one'])
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype == 'many2many'])
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'value_mapping'])
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'date_adapt'])
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'expression'])
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'migrated_id'])
        target_fields.extend([x.target_field for x in self.field_mapping_ids if x.state==state and x.type == 'reference'])

        # Read and append source values of type 'field' and type not m2m
        _logger.info('Building none m2m field mapping...')
        source_model_data = source_model_obj.export_data(
            source_model_ids, source_fields)['datas']

        _logger.info('Building m2o field mapping...')
        # Read and append source values of type 'field' and type m2m
        source_fields_m2o = [x.id for x in self.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype == 'many2one']
        for field_id in source_fields_m2o:
            field = field_mapping_obj.browse(field_id)
            field_model = field.source_field_id.relation
            model_id = model_obj.search([('model','=',field_model),('type','ilike','source')])
            field_action = False
            if model_id:
                field_action = action_obj.search([('source_model_id','=',model_id[0].id)])
            if field_action:
                field_action = field_action[0]
                for source_data_record in source_model_data:
                    source_data_m2o = source_model_obj.export_data([int(source_data_record[0])], ['.id', field.source_field, field.source_field.replace('/','.')])['datas']
                    new_field_value = False
                    if field_action.target_id_type == 'source_id' and source_data_m2o[0][1]:
                        new_field_value = source_data_m2o[0][1]
                    elif field_action.target_id_type == 'builded_id' and source_data_m2o[0][2]:
                        new_field_value = '%s_%s' % (field_action.target_id_prefix, str(source_data_m2o[0][2]))
                    source_data_record.append(new_field_value)

        _logger.info('Building m2m field mapping...')
        # Read and append source values of type 'field' and type m2m
        source_fields_m2m = [x.id for x in self.field_mapping_ids if x.state==state and x.type == 'field' and x.source_field_id.ttype == 'many2many']
        for field_id in source_fields_m2m:
            field = field_mapping_obj.browse(field_id)
            field_model = field.source_field_id.relation
            model_id = model_obj.search([('model','=',field_model),('type','ilike','source')])
            field_action = False
            if model_id:
                field_action = action_obj.search([('source_model_id','=',model_id[0].id)])
            if field_action:
                field_action = field_action[0]
                model_data_obj = source_connection.model('ir.model.data')
                for source_data_record in source_model_data:
                    source_data_m2m = source_model_obj.export_data([int(source_data_record[0])], ['.id', field.source_field])['datas']
                    new_field_value = False
                    for readed_record in source_data_m2m:
                        if readed_record[1]:
                            for value in readed_record[1].split(','):
                                value_id = model_data_obj.search([('model','ilike',field.source_field_id.relation),('name','ilike',value.split('.')[-1])])
                                if value_id:
                                    value_id = model_data_obj.export_data([value_id[0]], ['.id', 'res_id'])['datas']
                                    value_id = value_id[0][1]
                                if field_action.target_id_type == 'source_id' and value:
                                    new_field_value = value
                                elif field_action.target_id_type == 'builded_id' and value_id:
                                    if new_field_value:
                                        new_field_value = new_field_value + ',' + '%s_%s' % (field_action.target_id_prefix, str(value_id))
                                    else:
                                        new_field_value = '%s_%s' % (field_action.target_id_prefix, str(value_id))
                    source_data_record.append(new_field_value)

        _logger.info('Building value mapping mapping...')
        # Read and append source values of type 'value_mapping'
        source_fields_value_mapping = [x.source_field for x in self.field_mapping_ids if x.state==state and x.type == 'value_mapping']
        #print 'source_fields_value_mapping', source_fields_value_mapping
        source_data_value_mapping = source_model_obj.export_data(source_model_ids, source_fields_value_mapping)['datas']
        #print 'source_data_value_mapping', source_data_value_mapping
        source_value_mapping_id = [x.value_mapping_field_id.id for x in self.field_mapping_ids if x.state==state and x.type == 'value_mapping']
        #print 'source_value_mapping_id', source_value_mapping_id
        for readed_record, source_data_record in zip(source_data_value_mapping, source_model_data):
            target_record = []
            for field_value, value_mapping_id in zip(readed_record, source_value_mapping_id):
                new_field_value = False
                value_mapping = value_mapping_field_obj.browse(
                    value_mapping_id)
                # TODO mejorar esta cosa horrible, no hace falta guardar en dos clases separadas, deberia usar una sola para selection y para id
                if value_mapping.type == 'id':
                    new_field = value_mapping_field_detail_obj.search([
                        ('source_external_model_record_id.ext_id', '=', field_value),
                        ('value_mapping_field_id', '=', value_mapping_id)],
                        limit=1)
                    # if new_fields:
                    new_field_value = new_field.target_external_model_record_id.ext_id
                elif value_mapping.type == 'selection':
                    new_field = value_mapping_field_detail_obj.search([
                        ('source_value_id.ext_id', '=', field_value),
                        ('value_mapping_field_id', '=', value_mapping_id)],
                        limit=1)
                    new_field_value = new_field.target_value_id.ext_id
                # Convertimos a false todos aquellos mapeos al que no se les asigno pareja
                # Si el modelo permite valores false va a andar bien, si no va a dar el error y debera mapearse
                if new_field_value is None:
                    new_field_value = False
                target_record.append(new_field_value)
            source_data_record.extend(target_record)

        _logger.info('Building date adapt...')
        # Read and append source values of type 'date_adapt'
        source_fields_date_adapt = [x.source_field for x in self.field_mapping_ids if x.state==state and x.type == 'date_adapt']
        source_data_date_adapt = source_model_obj.export_data(source_model_ids, source_fields_date_adapt)['datas']
        source_mapping_date_adapt = [x for x in self.field_mapping_ids if x.state==state and x.type == 'date_adapt']
        for readed_record, source_data_record in zip(source_data_date_adapt, source_model_data):
            target_record = []
            for field_value, source_mapping in zip(readed_record, source_mapping_date_adapt):
                if source_mapping.source_field_id.ttype == 'datetime' and field_value:
                    if source_mapping.target_field_id.ttype == 'date':
                        # TODO, no estoy seguro si esta forma de truncarlo funciona bien
                        field_value = field_value[:10]
                if source_mapping.source_field_id.ttype == 'date' and field_value:
                    if source_mapping.target_field_id.ttype == 'datetime':
                        field_value = self.date_to_datetime(field_value)
                target_record.append(field_value)
            source_data_record.extend(target_record)

        _logger.info('Building expressions...')
        field_mapping_expression_ids = [x.id for x in self.field_mapping_ids if x.state==state and x.type == 'expression']
        if field_mapping_expression_ids:
            for rec in source_model_data:
                rec_id = rec[0]
                expression_results = field_mapping_obj.browse(
                    field_mapping_expression_ids).run_expressions(
                        int(rec_id),
                        source_connection,
                        target_connection)
                rec.extend(expression_results)

        _logger.info('Building migrated ids...')
        field_mapping_migrated_id_ids = [x.id for x in self.field_mapping_ids if x.state==state and x.type == 'migrated_id']
        if field_mapping_migrated_id_ids:
            for rec in source_model_data:
                rec_id = rec[0]
                migrated_id_results = field_mapping_obj.browse(
                    field_mapping_migrated_id_ids).get_migrated_id(
                        int(rec_id),
                        source_connection,
                        target_connection)
                rec.extend(migrated_id_results)

        _logger.info('Building reference fields...')
        field_mapping_reference_ids = [x.id for x in self.field_mapping_ids if x.state==state and x.type == 'reference']
        if field_mapping_reference_ids:
            for rec in source_model_data:
                rec_id = rec[0]
                reference_results = field_mapping_obj.browse(
                    field_mapping_reference_ids).get_reference(
                        int(rec_id), source_connection, target_connection)
                _logger.info('Reference_results: %s' % reference_results)
                rec.extend(reference_results)

        _logger.info('Removing auxliaria .id')
        target_model_data = []
        #print source_model_data
        #print ''
        for record in source_model_data:
            if self.target_id_type == 'source_id':
                target_model_data.append(record[1:])
            elif self.target_id_type == 'builded_id':
                target_model_data.append(['%s_%s' % (
                    self.target_id_prefix, str(record[0]))] + record[2:])

        try:
            _logger.info('Loadding Data...')
            import_result = target_model_obj.load(
                target_fields, target_model_data)
            vals = {'log': import_result}
        except:
            error = sys.exc_info()
            print error
            vals = {'log': error}

        self.write(vals)
        self.target_model_id.get_records(target_connection)

    @api.multi
    def order_actions(self, exceptions=None):
        _logger.info('Lines to order %i' % len(self.ids))
        if exceptions is None:
            exceptions = []
        # field_mapping_obj = self.pool.get('etl.field_mapping')
        ordered_actions = []
        ordered_ids = []

        # We exclude de exceptions
        unordered_ids = self.search([
            ('id', 'in', self.ids),
            ('source_model_id.model', 'not in', exceptions)]).ids
        _logger.info('Request IDS: %s' % str(self.ids))
        _logger.info('Request IDS without exceptions: %s' % str(unordered_ids))

        actions_to_order = [
            x.source_model_id.model for x in self.browse(unordered_ids)]
        _logger.info('Actions_to_order %s' % actions_to_order)
        count = 0
        count_max = len(self) * 2
        while unordered_ids and (count < count_max):
            count += 1
            rec = self.browse(unordered_ids[0])
            action_clean_dependecies = []
            many2one_mappings = self.env['etl.field_mapping'].search([
                ('action_id', '=', rec.id),
                ('source_field_id.ttype', '=', 'many2one'),
                ('state', 'in', ['to_analyze', 'enabled', 'on_repeating'])])
            for mapping in many2one_mappings:
                if (mapping.source_field_id.relation not in action_clean_dependecies) and (mapping.source_field_id.relation in actions_to_order):
                    if not(mapping.source_field_id.relation == rec.source_model_id.model):
                        action_clean_dependecies.append(mapping.source_field_id.relation)
                    # else:
                        # TODO usar este dato para algo! para macar la clase por ejemplo
            _logger.info('Model: %s, depenencias: %s' % (
                rec.source_model_id.model, action_clean_dependecies))
            dependecies_ok = True
            for action_dependecy in action_clean_dependecies:
                if (action_dependecy not in ordered_actions) and (action_dependecy not in exceptions):
                    dependecies_ok = False
                    break
            unordered_ids.remove(rec.id)
            if dependecies_ok:
                _logger.info('Dependency ok!')
                ordered_ids.append(rec.id)
                ordered_actions.append(rec.source_model_id.model)
            else:
                _logger.info('Break, dependency false!')
                unordered_ids.append(rec.id)

        _logger.info('Unordered Models: %s' % str(unordered_ids))
        _logger.info('New Order: %s' % str(ordered_actions))

        # Add sequence to exception actions
        sequence = 0
        for exception in exceptions:
            exception_action_ids = self.search([
                ('id', 'in', self.ids),
                ('source_model_id.model', '=', exception)])
            sequence += 10
            vals = {
                'sequence': sequence,
            }
            exception_action_ids.write(vals)

        # Add sequence to ordered actions
        sequence = 500
        for ordered_action in self.browse(ordered_ids):
            sequence += 10
            vals = {
                'sequence': sequence,
            }
            ordered_action.write(vals)
        return [unordered_ids, ordered_ids]

    @api.model
    def date_to_datetime(self, userdate):
        """ Convert date values expressed in user's timezone to
        server-side UTC timestamp, assuming a default arbitrary
        time of 12:00 AM - because a time is needed.

        :param str userdate: date string in in user time zone
        :return: UTC datetime string for server-side use
        """
        # TODO: move to fields.datetime in server after 7.0
        user_date = datetime.strptime(userdate, DEFAULT_SERVER_DATE_FORMAT)
        context = self._context
        if context and context.get('tz'):
            tz_name = context['tz']
        else:
            tz_name = self.env['res.users'].browse(SUPERUSER_ID).tz
            print tz_name
            #tz_name = tz_name[0]
        if tz_name:
            utc = pytz.timezone('UTC')
            context_tz = pytz.timezone(tz_name)
            #user_datetime = user_date + relativedelta(hours=12.0)
            local_timestamp = context_tz.localize(user_date, is_dst=False)
            user_datetime = local_timestamp.astimezone(utc)
            return user_datetime.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        return user_date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
