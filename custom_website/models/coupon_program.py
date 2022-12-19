# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

import ast
#from odoo.addons.coupon.models.coupon import Coupon as base_coupon

class CouponProgram(models.Model):
    _inherit = 'coupon.program'

    rule_maximum_amount = fields.Float(default=0.0, help="Maximum required amount to get the reward")
    rule_maximum_amount_tax_inclusion = fields.Selection([
        ('tax_included', 'Tax Included'),
        ('tax_excluded', 'Tax Excluded')], default="tax_included")

    def _check_promo_code(self, order, coupon_code):
        message = {}
        if self.maximum_use_number != 0 and self.total_order_count >= self.maximum_use_number:
            message = {'error': _('Promo code %s has been expired.') % (coupon_code)}
        elif not self._filter_on_mimimum_amount(order):
            message = {'error': _(
                'A minimum of %(amount)s %(currency)s should be purchased to get the reward',
                amount=self.rule_minimum_amount,
                currency=self.currency_id.name
            )}

        elif not self._filter_on_maximum_amount(order):
            message = {'error': _(
                'A maximum of %(amount)s %(currency)s should be purchased to get the reward',
                amount=self.rule_maximum_amount,
                currency=self.currency_id.name
            )}
        elif self.promo_code and self.promo_code == order.promo_code:
            message = {'error': _('The promo code is already applied on this order')}
        elif self in order.no_code_promo_program_ids:
            message = {'error': _('The promotional offer is already applied on this order')}
        elif not self.active:
            message = {'error': _('Promo code is invalid')}
        elif self.rule_date_from and self.rule_date_from > fields.Datetime.now():
            tzinfo = self.env.context.get('tz') or self.env.user.tz or 'UTC'
            locale = self.env.context.get('lang') or self.env.user.lang or 'en_US'
            message = {'error': _('This coupon is not yet usable. It will be starting from %s') % (format_datetime(self.rule_date_from, format='short', tzinfo=tzinfo, locale=locale))}
        elif self.rule_date_to and fields.Datetime.now() > self.rule_date_to:
            message = {'error': _('Promo code is expired')}
        elif order.promo_code and self.promo_code_usage == 'code_needed':
            message = {'error': _('Promotionals codes are not cumulative.')}
        elif self._is_global_discount_program() and order._is_global_discount_already_applied():
            message = {'error': _('Global discounts are not cumulative.')}
        elif self.promo_applicability == 'on_current_order' and self.reward_type == 'product' and not order._is_reward_in_order_lines(self):
            message = {'error': _('The reward products should be in the sales order lines to apply the discount.')}
        elif not self._is_valid_partner(order.partner_id):
            message = {'error': _("The customer doesn't have access to this reward.")}
        elif not self._filter_programs_on_products(order):
            message = {'error': _("You don't have the required product quantities on your sales order. If the reward is same product quantity, please make sure that all the products are recorded on the sales order (Example: You need to have 3 T-shirts on your sales order if the promotion is 'Buy 2, Get 1 Free'.")}
        elif self.promo_applicability == 'on_current_order' and not self.env.context.get('applicable_coupon'):
            applicable_programs = order._get_applicable_programs()
            if self not in applicable_programs:
                message = {'error': _('At least one of the required conditions is not met to get the reward!')}
        return message

    def _filter_on_maximum_amount(self, order):
        
        no_effect_lines = order._get_no_effect_on_threshold_lines()
        order_amount = {
            'amount_untaxed' : order.amount_untaxed - sum(line.price_subtotal for line in no_effect_lines),
            'amount_tax' : order.amount_tax - sum(line.price_tax for line in no_effect_lines)
        }
        program_ids = list()
        for program in self:
            if program.reward_type != 'discount':
                # avoid the filtered
                lines = self.env['sale.order.line']
            else:
                lines = order.order_line.filtered(lambda line:
                    line.product_id == program.discount_line_product_id or
                    line.product_id == program.reward_id.discount_line_product_id or
                    (program.program_type == 'promotion_program' and line.is_reward_line)
                )
            untaxed_amount = order_amount['amount_untaxed'] - sum(line.price_subtotal for line in lines)
            tax_amount = order_amount['amount_tax'] - sum(line.price_tax for line in lines)
            program_amount = program._compute_program_amount('rule_maximum_amount', order.currency_id)
            if program.rule_maximum_amount_tax_inclusion == 'tax_included' and program_amount >= (untaxed_amount + tax_amount) or program_amount >= untaxed_amount:
                program_ids.append(program.id)

        return self.browse(program_ids)

class Coupon(models.Model):
    _inherit = 'coupon.coupon'

    def _check_coupon_code_verify(self, order_date, partner_id, **kwargs):
        """ Check the validity of this single coupon.
            :param order_date Date:
            :param partner_id int | boolean:
        """
        self.ensure_one()
        message = {}
        if self.state == 'used':
            message = {'error': _('This coupon has already been used (%s).') % (self.code)}
        elif self.state == 'reserved':
            message = {'error': _('This coupon %s exists but the origin sales order is not validated yet.') % (self.code)}
        elif self.state == 'cancel':
            message = {'error': _('This coupon has been cancelled (%s).') % (self.code)}
        elif self.state == 'expired' or (self.expiration_date and self.expiration_date < order_date):
            message = {'error': _('This coupon is expired (%s).') % (self.code)}
        elif not self.program_id.active:
            message = {'error': _('The coupon program for %s is in draft or closed state') % (self.code)}
        elif self.partner_id and self.partner_id.id != partner_id:
            message = {'error': _('Invalid partner.')}
        return message

    def _check_coupon_code(self, order_date, partner_id, **kwargs):
        message = self._check_coupon_code_verify(order_date, partner_id, **kwargs)
        #message = super(base_coupon, self)._check_coupon_code(order_date, partner_id, **kwargs)
        order = kwargs.get('order', False)
        if message.get('error', False) or not order:
            return message

        applicable_programs = order._get_applicable_programs()
        # Minimum requirement should not be checked if the coupon got generated by a promotion program (the requirement should have only be checked to generate the coupon)
        if self.program_id.program_type == 'coupon_program' and not self.program_id._filter_on_mimimum_amount(order):
            message = {'error': _(
                'A minimum of %(amount)s %(currency)s should be purchased to get the reward',
                amount=self.program_id.rule_minimum_amount,
                currency=self.program_id.currency_id.name
            )}

        elif self.program_id.program_type == 'coupon_program' and not self.program_id._filter_on_maximum_amount(order):
            message = {'error': _(
                'A maximum of %(amount)s %(currency)s should be purchased to get the reward',
                amount=self.program_id.rule_maximum_amount,
                currency=self.program_id.currency_id.name
            )}

        elif self.program_id in order.applied_coupon_ids.mapped('program_id'):
            message = {'error': _('A Coupon is already applied for the same reward')}
        elif self.program_id._is_global_discount_program() and order._is_global_discount_already_applied():
            message = {'error': _('Global discounts are not cumulable.')}
        elif self.program_id.reward_type == 'product' and not order._is_reward_in_order_lines(self.program_id):
            message = {'error': _('The reward products should be in the sales order lines to apply the discount.')}
        elif not self.program_id._is_valid_partner(order.partner_id):
            message = {'error': _("The customer doesn't have access to this reward.")}
        # Product requirement should not be checked if the coupon got generated by a promotion program (the requirement should have only be checked to generate the coupon)
        elif self.program_id.program_type == 'coupon_program' and not self.program_id._filter_programs_on_products(order):
            message = {'error': _("You don't have the required product quantities on your sales order. All the products should be recorded on the sales order. (Example: You need to have 3 T-shirts on your sales order if the promotion is 'Buy 2, Get 1 Free').")}
        else:
            if self.program_id not in applicable_programs and self.program_id.promo_applicability == 'on_current_order':
                message = {'error': _('At least one of the required conditions is not met to get the reward!')}
        return message
