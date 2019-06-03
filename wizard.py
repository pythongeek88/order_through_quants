# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import logging
_logger = logging.getLogger(__name__)

class OrderQuantForStockQuant(models.Model):
    _inherit = "stock.quant"

    quantity_to_order = fields.Float(string="Quantity to order", digits=(12, 2), default=1)

    @api.constrains('quantity_to_order')
    def _check_quantity_to_order_less_than_qty(self):
        for r in self:
            if r.quantity_to_order > r.qty:
                raise exceptions.ValidationError("You can't order more, than we have on hand.")
            if not (r.quantity_to_order > 0):
                raise exceptions.ValidationError("You can't order zero or less.")


class Wizard(models.TransientModel):
    _name = 'new.wizard'
    customer = fields.Many2one('res.partner',
        string="Customer", required=True, default=lambda self: self.env.user)

    def _default_stock_quants(self):
            return self.env['stock.quant'].browse(self._context.get('active_ids'))

    stock_quant_ids = fields.Many2many('stock.quant',
            string="Stock quants", required=True, default=_default_stock_quants)

    


    @api.multi
    def confirm_order(self):
        for line in self.stock_quant_ids:
            _logger.debug('##########')
            # _logger.debug(line.location_id.name)
            values_for_new_order = {'partner_id' : self.customer.id, 'state': 'draft', 'product_id': line.product_id.id}
            # _logger.debug(values_for_new_order)
            new_order = self.env['sale.order'].create(values_for_new_order)

            values_order_product = {'order_id': new_order.id, 'product_id': line.product_id.id, 'product_uom_qty': line.quantity_to_order, 'product_uom': line.product_uom_id.id}
            # _logger.debug(values_order_product)
            new_order_line = self.env['sale.order.line'].create(values_order_product)

            new_order.action_confirm()
            # _logger.debug(new_order.state)

            # This stuff I tried:
            # _logger.debug(new_order.procurement_group_id)
            # _logger.debug(new_order.procurement_group_id.id)

            # values_procurement = {'origin': new_order.name, 'name': new_order.order_line.name, 'product_id': line.product_id.id, 'product_qty': line.quantity_to_order, 'product_uom': line.product_uom_id.id, 'state': 'confirmed'}
            # new_procurement_order = self.env['procurement.order'].create(values_procurement)
            # _logger.debug(new_procurement_order)

            # added_delivery_count = new_order.write({'procurement_group_id': 4})
            # # _logger.debug(added_delivery_count)
            # _logger.debug(new_order.delivery_count)
            # values = {'order_id': new_order.id, 'product_id': line.product_id.id, 'product_uom_qty': line.quantity_to_order, 'product_uom': line.product_uom_id.id}
            # _logger.debug(values)
            # new_order_line = self.env['sale.order.line'].create(values)
            # _logger.debug(new_order_line)


            # vals_delivery = {'partner_id' : self.customer.id, 'origin': new_order.name, 'picking_type_id': 4, 'location_id': line.location_id.id, 'location_dest_id': 9}
            # new_delivery = self.env['stock.picking'].create(vals_delivery)
            # _logger.debug(new_delivery)

            
            
