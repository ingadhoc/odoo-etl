# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning
import time
from openerp.tools.safe_eval import safe_eval as eval
import logging
_logger = logging.getLogger(__name__)


class field_mapping(models.Model):
    """"""

    _name = 'etl.field_mapping'
    _description = 'field_mapping'

    blocked = fields.Boolean(
        string='Blocked',
        default=False
        )
    state = fields.Selection(
        [(u'on_repeating', 'on_repeating'), (u'to_analyze', 'to_analyze'), (u'enabled', 'enabled'), (u'disabled', 'disabled'), (u'other_class', 'other_class')],
        string='State',
        required=True
        )
    type = fields.Selection(
        [(u'field', 'field'), (u'expression', 'expression'), (u'migrated_id', u'Migrated ID'), (u'value_mapping', u'Value Mapping'), (u'date_adapt', u'Date Adapt'), (u'reference', 'reference')],
        string='Source Type',
        default='field'
        )
    source_field_id = fields.Many2one(
        'etl.field',
        string='Source Field'
        )
    source_field = fields.Char(
        string='Source Exp.'
        )
    target_field_id = fields.Many2one(
        'etl.field',
        string='Target Field'
        )
    target_field = fields.Char(
        string='Target Exp.'
        )
    expression = fields.Text(
        string='Expression',
        default="context['result']= False"
        )
    value_mapping_field_id = fields.Many2one(
        'etl.value_mapping_field',
        string='Value Mapping Field'
        )
    model_field_id = fields.Many2one(
        'etl.field',
        string='Model Field'
        )
    model_field = fields.Char(
        string='Model Field Exp.'
        )
    note = fields.Html(
        string='Notes'
        )
    action_id = fields.Many2one(
        'etl.action',
        ondelete='cascade',
        string='Action',
        required=True
        )
    target_model_id = fields.Many2one(
        related='action_id.target_model_id',
        relation='etl.external_model',
        string='Target Model',
        )
    source_model_id = fields.Many2one(
        related='action_id.source_model_id',
        relation='etl.external_model',
        string='Source Model',
        )
    source_field_ttype = fields.Char(
        related='source_field_id.ttype',
        readonly=True,
        string='Source Type'
        )
    target_field_ttype = fields.Char(
        related='target_field_id.ttype',
        readonly=True,
        string='Target Type'
        )
    manager_id = fields.Many2one(
        related='action_id.manager_id',
        relation='etl.manager',
        readonly=True,
        string='Manager'
        )

    _constraints = [
    ]

    @api.onchange('source_field_id')
    def onchange_source_field(self):
        source_field = False
        if self.source_field_id:
            source_field = self.source_field_id.name
            if self.source_field_id.ttype in (
                    'many2one', 'many2many', 'one2many'):
                source_field += '/id'
        self.source_field = source_field

    @api.onchange('target_field_id')
    def onchange_target_field(self):
        target_field = False
        if self.target_field_id:
            target_field = self.target_field_id.name
            if self.target_field_id.ttype in (
                    'many2one', 'many2many', 'one2many'):
                target_field += '/id'
        self.target_field = target_field

    @api.multi
    def action_block(self):
        return self.write({'blocked': True})

    @api.multi
    def get_migrated_id(
            self, rec_id, source_connection=False, target_connection=False):
        '''Get migrated id for field ids  and one rec_id (from source database)
        For example, for field mapping ids'''
        result = []

        for field_mapping in self:
            if not source_connection or not target_connection:
                (source_connection, target_connection) = field_mapping.action_id.manager_id.open_connections()
            source_model_obj = source_connection.model(
                field_mapping.action_id.source_model_id.model)
            target_ir_model_data_obj = target_connection.model('ir.model.data')
            source_fields = [
                'id',
                field_mapping.source_field_id.name,
                field_mapping.model_field]
            _logger.info('Source_fields: %s' % source_fields)
            source_model_data = source_model_obj.export_data(
                [rec_id], source_fields)['datas']
            _logger.info('Source_model_data: %s' % source_model_data)
            target_id = False
            if source_model_data:
                source_id = source_model_data[0][1]
                try:
                    source_resource_obj = source_connection.model(
                        source_model_data[0][2])
                except:
                    target_id = False
                else:
                    source_reference = source_resource_obj.export_data(
                        [int(source_id)], ['id'])['datas']
                    if source_reference[0]:
                        source_reference_splited = source_reference[0][0].split(
                            '.', 1)
                        print 'source_reference_splited', source_reference_splited
                        if len(source_reference_splited) == 1:
                            module = False
                            external_ref = source_reference_splited[0]
                        else:
                            module = source_reference_splited[0]
                            external_ref = source_reference_splited[1]
                        try:
                            # cambiamos a esta manera fea porque el metodo de abajo no andaba
                            target_ids = target_ir_model_data_obj.search([(
                                'module', '=', module), ('name', '=', external_ref)])
                            target_ids = target_ir_model_data_obj.read(target_ids, ['res_id'])
                            if target_ids:
                                target_id = target_ids[0].get('res_id', False)
                            # target_id = target_ir_model_data_obj.get_object_reference(
                                # module, external_ref)[1]
                        except:
                            target_id = False
            result.append(target_id)
        return result

    @api.multi
    def get_reference(
            self, rec_id, source_connection=False, target_connection=False):
        '''Get reference for field ids  and one rec_id (from source database)
        For example, for field mapping ids'''

        result = []
        for field_mapping in self:
            if not source_connection or not target_connection:
                (source_connection, target_connection) = field_mapping.action_id.manager_id.open_connections()
            source_model_obj = source_connection.model(
                field_mapping.action_id.source_model_id.model)
            target_ir_model_data_obj = target_connection.model('ir.model.data')
            source_fields = [field_mapping.source_field_id.name]
            source_model_data = source_model_obj.read(
                [rec_id], source_fields)[0]
            target_id = False
            if source_model_data:
                source_reference = source_model_data[
                    field_mapping.source_field_id.name]
                if source_reference:
                    model, res_id = source_reference.split(',', 1)
                    try:
                        source_resource_obj = source_connection.model(model)
                    except:
                        target_id = False
                    else:
                        source_ext_id = source_resource_obj.export_data(
                            [res_id], ['id'])['datas']
                        if source_ext_id[0]:
                            source_ext_id_splited = source_ext_id[0][0].split(
                                '.', 1)
                            if len(source_ext_id_splited) == 1:
                                module = False
                                external_ref = source_ext_id_splited[0]
                            else:
                                module = source_ext_id_splited[0]
                                external_ref = source_ext_id_splited[1]
                            try:
                                target_id = target_ir_model_data_obj.get_object_reference(
                                    module, external_ref)[1]
                            except:
                                # Agregamos este nuevo try porque algunas veces module no es false si no que es como una cadena vacia
                                try:
                                    target_id = target_ir_model_data_obj.get_object_reference(
                                        '', external_ref)[1]
                                except:
                                    target_id = False
            target_reference = False
            if target_id:
                target_reference = model + ',' + str(target_id)
            result.append(target_reference)
        return result

    @api.multi
    def run_expressions(
            self, rec_id, source_connection=False, target_connection=False):
        result = []

        for field_mapping in self:
            expression_result = False
            if not source_connection or not target_connection:
                (source_connection, target_connection) = field_mapping.action_id.manager_id.open_connections()
            source_model_obj = source_connection.model(
                field_mapping.action_id.source_model_id.model)
            target_model_obj = target_connection.model(
                field_mapping.action_id.target_model_id.model)

            obj_pool = source_model_obj
            cxt = {
                'self': obj_pool,   #to be replaced by target_obj
                'source_obj': source_model_obj,
                'source_connection': source_connection,
                'target_obj': target_model_obj,
                'target_connection': target_connection,
                'rec_id': rec_id,
                'pool': self.pool,
                'time': time,
                'cr': self._cr,
                # copy context to prevent side-effects of eval
                'context': dict(self._context),
                'uid': self.env.user.id,
                'user': self.env.user,
            }
            if not field_mapping.expression:
                raise Warning(_(
                    'Warning. Type expression choosen buy not expression set'))
            # nocopy allows to return 'action'
            eval(field_mapping.expression.strip(), cxt, mode="exec")
            if 'result' in cxt['context']:
                expression_result = cxt['context'].get('result')
            result.append(expression_result)
        return result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
