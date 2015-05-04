# -*- coding: utf-8 -*-
from openerp.osv import fields, osv


class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'

    def _get_main_address(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for address in self.browse(cr, uid, ids, context=context):
            result = False
            if address.partner_id and address.partner_id.address:
                if address.partner_id.address[0].id == address.id:
                    result = True
            res[address.id] = result
        return res

    _columns = {
        # new migration fields
        'main_address': fields.function(
            _get_main_address, type='boolean', string='Main address?',
            store=True),
    }
