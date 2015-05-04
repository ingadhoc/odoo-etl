# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class manager(models.Model):
    """"""

    _name = 'etl.manager'
    _description = 'manager'

    name = fields.Char(
        string='Name',
        required=True
        )
    source_hostname = fields.Char(
        string='Source Hostname',
        required=True
        )
    source_port = fields.Integer(
        string='Source Port',
        required=True
        )
    source_database = fields.Char(
        string='Source Database',
        required=True
        )
    source_login = fields.Char(
        string='Source Login',
        required=True
        )
    source_password = fields.Char(
        string='Source Password',
        required=True
        )
    target_hostname = fields.Char(
        string='Target Hostname',
        required=True
        )
    target_port = fields.Integer(
        string='Target Port',
        required=True
        )
    target_database = fields.Char(
        string='Target Database',
        required=True
        )
    target_login = fields.Char(
        string='Target Login',
        required=True
        )
    target_password = fields.Char(
        string='Target Password',
        required=True
        )
    log = fields.Text(
        string='Log'
        )
    model_disable_default = fields.Text(
        string='Models Disabled by Default'
        )
    field_disable_default = fields.Text(
        string='Fields Disable by Default'
        )
    model_exception_words = fields.Char(
        string='Model Exception Words'
        )
    model_analyze_default = fields.Text(
        string='Models Analyze by Default'
        )
    note = fields.Html(
        string='Notes'
        )
    field_analyze_default = fields.Text(
        string='Fields Analize by Default'
        )
    repeating_models = fields.Text(
        string='Repeating Models'
        )
    field_disable_words = fields.Text(
        string='Fields Disable by Default Words'
        )
    modules_to_install = fields.Text(
        string='Modules To Install',
        default=[]
        )
    workflow_models = fields.Char(
        string='Models to delete Workflows',
        required=True,
        default='[]'
        )
    action_ids = fields.One2many(
        'etl.action',
        'manager_id',
        string='Actions',
        domain=[('state','in',['to_analyze','enabled'])]
        )
    external_model_ids = fields.One2many(
        'etl.external_model',
        'manager_id',
        string='External Models',
        readonly=True
        )
    value_mapping_field_ids = fields.One2many(
        'etl.value_mapping_field',
        'manager_id',
        string='Value Mapping Fields'
        )

    _constraints = [
    ]

    @api.one
    def open_connections(self):
        """"""
        raise NotImplementedError

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
