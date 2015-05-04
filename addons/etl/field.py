# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class field(models.Model):
    """"""

    _name = 'etl.field'
    _description = 'field'

    name = fields.Char(
        string='Name',
        required=True
        )
    field_description = fields.Char(
        string='Field Description',
        required=True
        )
    relation = fields.Char(
        string='Relation'
        )
    relation_field = fields.Char(
        string='Relation Field'
        )
    ttype = fields.Char(
        string='Type',
        required=True
        )
    required = fields.Char(
        string='Required'
        )
    function = fields.Char(
        string='Function'
        )
    model_id = fields.Many2one(
        'etl.external_model',
        ondelete='cascade',
        string='Model'
        )

    _constraints = [
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
