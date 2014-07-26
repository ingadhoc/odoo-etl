# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class task(osv.osv):
    _inherit = "project.task"

    def _check_dates(self, cr, uid, ids, context=None):

        return True