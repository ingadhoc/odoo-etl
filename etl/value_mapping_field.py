# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class value_mapping_field(models.Model):
    """"""

    _name = 'etl.value_mapping_field'
    _description = 'value_mapping_field'

    name = fields.Char(
        string='Field Name',
        required=True
        )
    type = fields.Selection(
        [(u'id', u'Id'), (u'char', u'Char (not implemented yet)'), (u'selection', u'Selection')],
        string='Type',
        required=True
        )
    source_model_id = fields.Many2one(
        'etl.external_model',
        string='Source Model'
        )
    target_model_id = fields.Many2one(
        'etl.external_model',
        string='Target Model'
        )
    log = fields.Text(
        string='log'
        )
    value_mapping_field_detail_ids = fields.One2many(
        'etl.value_mapping_field_detail',
        'value_mapping_field_id',
        string='Details'
        )
    value_mapping_field_value_ids = fields.One2many(
        'etl.value_mapping_field_value',
        'value_mapping_field_id',
        string='Mapping Values'
        )
    manager_id = fields.Many2one(
        'etl.manager',
        ondelete='cascade',
        string='manager_id',
        required=True
        )

    _constraints = [
    ]

    @api.one
    def map_record(self):
        value_mapping_data = []
        for source_record in self.source_model_id.external_model_record_ids:
            domain = [
                ('external_model_id', '=', self.target_model_id.id),
                ('name', 'ilike', source_record.name)]
            target_record = self.env[
                'etl.external_model_record'].search(domain, limit=1)
            value_mapping_data.append([
                'value_mapping_' + str(source_record.id),
                source_record.id,
                target_record and target_record.id or False,
                self.id,
                ])

        value_mapping_fields = [
            'id',
            'source_external_model_record_id/.id',
            'target_external_model_record_id/.id',
            'value_mapping_field_id/.id']
        import_result = self.env['etl.value_mapping_field_detail'].load(
            value_mapping_fields, value_mapping_data)

        # write log and domain if active field exist
        self.log = import_result

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
