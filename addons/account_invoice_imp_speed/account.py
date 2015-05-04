# -*- coding: utf-8 -*-
from openerp import models, api


class invoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends()
    def re_compute_stored_values(self):
        print 'invoice.ids', self.ids
        for invoice in self.search([]):
            print 'invoice lines for invoice', invoice
            invoice.invoice_line._compute_price()
        for invoice in self.search([]):
            print 'invoice', invoice
            invoice._compute_amount()
            invoice._compute_reconciled()
            # invoice._compute_residual() #este se calcula automaticamente cuando se cambia el anterior

    @api.one
    @api.depends()
    def _compute_amount(self):
        return super(invoice, self)._compute_amount()

    @api.one
    @api.depends(
    )
    def _compute_residual(self):
        return super(invoice, self)._compute_residual()

    @api.one
    @api.depends()
    def _compute_reconciled(self):
        return super(invoice, self)._compute_reconciled()


class invoice_line(models.Model):
    _inherit = "account.invoice.line"

    @api.one
    @api.depends()
    def _compute_price(self):
        return super(invoice_line, self)._compute_price()
