# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from ast import literal_eval
import logging
_logger = logging.getLogger(__name__)


class external_model(models.Model):
    """"""

    _name = 'etl.external_model'
    _description = 'external_model'

    _order = "sequence"

    sequence = fields.Integer(
        string='Sequence',
        readonly=True
        )
    type = fields.Selection(
        [(u'source', u'Source'), (u'target', u'Target')],
        string='Type',
        readonly=True,
        required=True
        )
    name = fields.Char(
        string='Name',
        readonly=True,
        required=True
        )
    model = fields.Char(
        string='Model',
        readonly=True,
        required=True
        )
    order = fields.Integer(
        string='Order',
        readonly=True
        )
    records = fields.Integer(
        string='Records',
        readonly=True
        )
    fields_to_read = fields.Char(
        string='Fields to read',
        default=['name']
        )
    field_ids = fields.One2many(
        'etl.field',
        'model_id',
        string='Fields',
        readonly=True
        )
    source_action_ids = fields.One2many(
        'etl.action',
        'source_model_id',
        string='source_action_ids'
        )
    target_action_ids = fields.One2many(
        'etl.action',
        'target_model_id',
        string='target_action_ids'
        )
    manager_id = fields.Many2one(
        'etl.manager',
        ondelete='cascade',
        string='Manager',
        readonly=True,
        required=True
        )
    external_model_record_ids = fields.One2many(
        'etl.external_model_record',
        'external_model_id',
        string='external_model_record_ids'
        )

    _constraints = [
    ]

    def _name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('model', operator, name), ('name', operator, name)]
        return self.name_get(cr, name_get_uid or uid,
                             super(external_model, self).search(cr, uid, domain, limit=limit, context=context),
                             context=context)

    @api.one
    def read_records(self):
        '''Function that reads external id and name field from an external
        model and save them in migrator database'''
        (source_connection, target_connection) = self.manager_id.open_connections()
        if self.type == 'source':
            connection = source_connection
        else:
            connection = target_connection

        fields_to_read = []
        if self.fields_to_read:
            fields_to_read = literal_eval(self.fields_to_read)

        record_fields = ['.id', 'id']
        record_fields.extend(fields_to_read)

        external_model_obj = connection.model(self.model)
        external_model_record_ids = external_model_obj.search([])
        external_model_record_data = external_model_obj.export_data(
            external_model_record_ids, record_fields)['datas']

        new_external_model_record_data = []
        for record in external_model_record_data:
            # take out item o and init new_record with our own ext id
            new_record = [
                'model%i_record_%s' % (self.id, record.pop(0))]
            # append readed external id 'id' to new record
            new_record.append(record.pop(0))
            # buid name wit readed fields
            name = ''
            # record = record.decode("utf-8")
            name = '; '.join([x for x in record if x])
            new_record.append(name)
            # append model id
            new_record.append(self.id)
            new_external_model_record_data.append(new_record)
        external_model_record_fields = [
            'id',
            'ext_id',
            'name',
            'external_model_id/.id']
        # load records
        self.env['etl.external_model_record'].load(
            external_model_record_fields, new_external_model_record_data)

    @api.multi
    def read_fields_button(self):
        return self.read_fields(False)

    @api.multi
    def read_fields(self, connection=False):
        ''' Get fields for external models'''
        field_fields = [
            'id',
            'model_id/.id',
            'field_description',
            'name',
            'relation',
            'required',
            'ttype',
            'function']
        model_field_data = []
        for model in self:
            _logger.info('Reading fields %s database, model: %s' % (
                model.type, model.name))
            if not connection:
                (source_connection, target_connection) = model.manager_id.open_connections()
                if model.type == 'source':
                    connection = source_connection
                elif model.type == 'target':
                    connection = target_connection
                else:
                    raise Warning(_('Error getting connection'))
            external_model_obj = connection.model(model.model)
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

                    field_data = [
                        'field_model_%s_%s' % (str(model.id), name),
                        model.id,
                        string,
                        name,
                        relation,
                        required,
                        ttype,
                        function
                        ]
                    model_field_data.append(field_data)
        _logger.info('Writing fields data...')
        self.env['etl.field'].load(field_fields, model_field_data)

    @api.one
    def get_records(self, connection):
        try:
            model_obj = connection.model(self.model)
            model_ids = model_obj.search([])
            vals = {'records': len(model_ids)}
            _logger.info('%i records on model %s' % (
                len(model_ids), self.name))
            self.write(vals)
        except:
            _logger.error('Error getting records')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
