# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
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
    type = fields.Selection(
        related='model_id.type',
        string='Type',
        readonly=True,
        )

    _constraints = [
    ]

    def _name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100, name_get_uid=None):
        if args is None:
            args = []
        domain = args + ['|', ('field_description', operator, name), ('name', operator, name)]
        return self.name_get(cr, name_get_uid or uid,
                             super(field, self).search(cr, uid, domain, limit=limit, context=context),
                             context=context)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
