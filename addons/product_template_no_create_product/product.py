# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class product_template(osv.osv):
    _inherit = "product.template"

    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        context['create_product_product'] = True
        return super(product_template, self).create(cr, uid, vals, context=context)