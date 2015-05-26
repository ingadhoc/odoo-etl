# -*- coding: utf-8 -*-
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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
