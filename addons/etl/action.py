# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class action(models.Model):
    """"""

    _name = 'etl.action'
    _description = 'action'

    _order = "sequence"

    blocked = fields.Boolean(
        string='Blocked'
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
        string='Repeating Action?'
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
        default='source_id'
        )
    from_rec_id = fields.Integer(
        string='From Record'
        )
    to_rec_id = fields.Integer(
        string='To Record'
        )
    target_id_prefix = fields.Char(
        string='target_id_prefix'
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
        string='Fields Mapping'
        )
    source_model_id = fields.Many2one(
        'etl.external_model',
        string='Source Model',
        required=True
        )
    target_model_id = fields.Many2one(
        'etl.external_model',
        string='Target Model'
        )

    _constraints = [
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
