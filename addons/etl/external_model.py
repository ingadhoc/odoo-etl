# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


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

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
