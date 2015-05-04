# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


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

    _constraints = [
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
