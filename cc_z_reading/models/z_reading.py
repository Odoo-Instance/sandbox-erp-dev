import base64
from email.policy import default
import logging
import re
from datetime import timedelta, datetime
from functools import partial
from itertools import groupby
from xml.etree.ElementTree import tostring

import psycopg2
import pytz
from odoo import _, api, fields, models
from odoo.osv.expression import AND


class ZReading(models.Model):
	_name = 'cc_z_reading.z_reading'
	_description = 'Model for Z-Reading'

	def _default_start_date(self):
		"""
		Find the last end date of the last z-reading
		Set as default start date

		arrange domain by date (desc)
		limit to 5 (should we limit? what if there are multiple records?)

		"""
		arrange_z_reading_ids = self.search([], order='end_date desc')
		if arrange_z_reading_ids:
			return arrange_z_reading_ids[0].end_date

		else:
			return datetime.now()

	start_date = fields.Datetime(required=True, default=_default_start_date)
	end_date = fields.Datetime(required=True, default=fields.Datetime.now)
	pos_config_ids = fields.Many2many('pos.config', 'z_reading_configs',
									  default=lambda s: s.env['pos.config'].search([]))
	total_sales = fields.Float(default=0, compute="_fetch_total_sales")
	# total_sales_ids = fields.Many2many('pos.session')
	total_returns = fields.Float(default=0, compute="_fetch_total_returns")
	total_returns_ids = fields.Many2many('pos.order')
	total_voids = fields.Float(default=0, compute="_fetch_total_voids")
	total_discounts = fields.Float(default=0, compute="_fetch_total_discounts")
	subtotal = fields.Float(default=0, compute="_compute_subtotal")

	vatable_sales = fields.Float(default=0, compute="_fetch_vatable_sales")
	vat_12 = fields.Float(default=0, compute="_fetch_vat_12")
	vat_exempt_sales = fields.Float(
		default=0, compute="_fetch_vat_exempt_sales")
	zero_rated_sales = fields.Float(
		default=0, compute="_fetch_zero_rated_sales")
	register_total = fields.Float(default=0, compute="_compute_register_total")

	beginning_reading = fields.Float(default=0, compute="_compute_reading")
	ending_reading = fields.Float(default=0, compute="_compute_reading")
	payments_ids = fields.Many2many('pos.payment', 'z_reading_payments')

	crm_team_id = fields.Many2one('crm.team')
	session_ids = fields.Many2many('pos.session', 'z_reading_sessions')
	
	# PLEASE UPDATE THE FIELD BELOW, ONCE THE MODULE FOR PWD AND SC DISCOUNTS ARE COMPLETED
	# PLEASE ADD NEW FIELDS FOR FETCHING THE CORRESPONDING DISCOUNTS:
	# # # * SC/PWD 5%
	# # # * SC 20%
	# # # * PWD 20%
	regular_discount = fields.Float(
		default=0, compute="_fetch_regular_discount")

	def is_available(self, date_start, date_stop, crm_team_id, order=None):
		if crm_team_id:
			domain = ["&", ["start_at", ">=", fields.Datetime.to_string(date_start)], ["stop_at", "<=", fields.Datetime.to_string(
				date_stop)], ["state", "=", "closed"], ['crm_team_id.name', '=', crm_team_id[0].name]]
			sessions = self.env['pos.session'].search(domain, order=order)

			if sessions:
				self.session_ids = sessions
				return sessions

	def get_payments(self, date_start=False, date_stop=False):
		"""
			get sessions in between start and end dates
			get order ids from sessions
			get payment ids from order ids
			if true > execute sql
			else, set payments to empty

			return payments

		"""
		sessions = self.is_available(date_start, date_stop, self.crm_team_id)
		if sessions:
			orders = sessions.order_ids
			payment_ids = self.env["pos.payment"].search(
				[('pos_order_id', 'in', orders.ids)]).ids
			if payment_ids:
				self.env.cr.execute("""
					SELECT method.name, sum(amount) total
					FROM pos_payment AS payment,
						pos_payment_method AS method
					WHERE payment.payment_method_id = method.id
						AND payment.id IN %s
					GROUP BY method.name
				""", (tuple(payment_ids),))
				payments = self.env.cr.dictfetchall()
				self.payments_ids = payment_ids
				
				print("Payments > ", payments)
			else:
				payments = []
				print("Payments > ", payments)
			return {
				'payments': payments
			}

		else:
			payments = []
			print("Payments > ", payments)
			return {
				'payments': payments
			}

	@api.depends('start_date', 'end_date')
	def _compute_reading(self):
		for r in self:
			order = "start_at asc"
			sessions = r.is_available(
				r.start_date, r.end_date, r.crm_team_id, order)

			"""
			Add domain to session per calculations; so that the orders that will be computed
			will be pertaining to sessions that are closed and fits the start and end date
			of the z-reading.

			Add start balance to total payments amount to get the end balance.

			Check if sessions are in order - where the oldest date is first
			"""

			print("Sessions >", sessions)

			if sessions:
				r.beginning_reading = round(
					sessions[0].cash_register_id.balance_start, 2)
				print("Starting Balance >",
					sessions[0].cash_register_id.balance_start)
				print("Total Payments Amount >",
					sessions[0].total_payments_amount)

				end_balance_total = 0
				for session in sessions:
					end_balance_total += session.total_payments_amount
					print("Starting Balance per session >",
						session.cash_register_id.balance_start)
					print("Total Payments Amount per session >",
						session.total_payments_amount)

				r.ending_reading = round(
					end_balance_total + r.beginning_reading, 2)
				print("Total End Reading >", end_balance_total)
				print("Ending Balance >", end_balance_total +
					sessions[0].cash_register_id.balance_start)

			else:
				r.beginning_reading = 0
				r.ending_reading = 0
				print("There are no sessions.")

	@api.onchange('start_date')
	def _onchange_start_date(self):
		if self.start_date and self.end_date and self.end_date < self.start_date:
			self.end_date = self.start_date

	@api.onchange('end_date')
	def _onchange_end_date(self):
		if self.end_date and self.end_date < self.start_date:
			self.start_date = self.end_date

	@api.depends('start_date', 'end_date')
	def _fetch_total_returns(self):
		for r in self:

			sessions = r.is_available(r.start_date, r.end_date, r.crm_team_id)

			amount_total = 0
			total_returns_ids = []
			if sessions:
				for session in sessions:
					for order in session.order_ids:
						if order.amount_total:
							if order.amount_total < 0:
								total_returns_ids.append(order.id)
								print("Return Orders > ", order.id)
								amount_total += abs(order.amount_total)

			print("Total Return Ids > ", total_returns_ids)
			self.total_returns_ids = total_returns_ids
			r.total_returns = round(amount_total, 2)

	@api.depends('start_date', 'end_date', 'total_returns', 'total_discounts')
	def _fetch_total_sales(self):
		for r in self:
			sessions = r.is_available(r.start_date, r.end_date, r.crm_team_id)
			amount_total = 0
			if sessions:
				for session in sessions:
					for order in session.order_ids:
						amount_total += order.amount_total

			amount_total += r.total_returns + r.total_discounts
			r.total_sales = round(amount_total, 2)

			# amount_total = is taxed, is discounted, if - (refunded)
			# should be taxed, should not be discounted, should included refundable, should include voided


	@api.depends('start_date', 'end_date')
	def _fetch_total_voids(self):
		"""
			integrate void module later;
			this does nothing right now;
			will always give 0;
		"""
		for r in self:
			query = """
				SELECT SUM(amount_total)
				FROM pos_order
				WHERE NOT ('%s' > date_order OR '%s' < date_order) AND
				state = 'cancel'
			""" % (fields.Datetime.to_string(r.start_date), fields.Datetime.to_string(r.end_date))
			r.env.cr.execute(query)
			total_voids = r.env.cr.dictfetchall()
			if total_voids[0]['sum'] is None:
				r.total_voids = 0
			else:
				r.total_voids = round(total_voids[0]['sum'], 2)

	@api.depends('start_date', 'end_date')
	def _fetch_total_discounts(self):
		for r in self:
			sessions = r.is_available(r.start_date, r.end_date, r.crm_team_id)
			amount_total = 0
			if sessions:
				for session in sessions:
					for order in session.order_ids:
						for line in order.lines:
							amount_total += (line.qty * line.price_unit) * \
								(line.discount / 100)

			r.total_discounts = round(amount_total, 2)

	@api.depends('total_sales', 'total_returns', 'total_voids', 'total_discounts')
	def _compute_subtotal(self):
		for r in self:
			r.subtotal = round(
				(r.total_sales - (r.total_returns + r.total_voids + r.total_discounts)), 2)

	@api.depends('start_date', 'end_date', 'crm_team_id')
	def _fetch_vatable_sales(self):
		for r in self:
			sessions = r.is_available(r.start_date, r.end_date, r.crm_team_id)
			amount_total = 0

			if sessions:
				domain = ["&",
					  ["lines.tax_ids.tax_type", "=", "vatable"],
					  ["session_id", "in", sessions.ids]
					  ]
				orders = self.env['pos.order'].search(domain)
				for order in orders:
					for line in order.lines:
						amount_total += line.price_subtotal

			r.vatable_sales = round(amount_total, 2)

	@api.depends('start_date', 'end_date', 'crm_team_id')
	def _fetch_vat_12(self):
		for r in self:
			sessions = r.is_available(r.start_date, r.end_date, r.crm_team_id)
			amount_total = 0

			if sessions:
				domain = ["&",
					  ["lines.tax_ids.tax_type", "=", "vatable"],
					  ["session_id", "in", sessions.ids]
					  ]
				orders = self.env['pos.order'].search(domain)
				for order in orders:
					amount_total += order.amount_tax

			r.vat_12 = round(amount_total, 2)

	@api.depends('start_date', 'end_date', 'crm_team_id')
	def _fetch_vat_exempt_sales(self):
		for r in self:
			sessions = r.is_available(r.start_date, r.end_date, r.crm_team_id)
			amount_total = 0

			if sessions:
				domain = ["&",
					  ["lines.tax_ids.tax_type", "=", "vat_exempt"],
					  ["session_id", "in", sessions.ids]
					  ]
				orders = self.env['pos.order'].search(domain)
				for order in orders:
					for line in order.lines:
						amount_total += line.price_subtotal

			r.vat_exempt_sales = round(amount_total, 2)

	@api.depends('start_date', 'end_date', 'crm_team_id')
	def _fetch_zero_rated_sales(self):
		for r in self:
			sessions = r.is_available(r.start_date, r.end_date, r.crm_team_id)
			amount_total = 0

			if sessions:
				domain = ["&",
					  ["lines.tax_ids.tax_type", "=", "zero_rated"],
					  ["session_id", "in", sessions.ids]
					  ]
				orders = self.env['pos.order'].search(domain)
				for order in orders:
					for line in order.lines:
						amount_total += line.price_subtotal

			r.zero_rated_sales = round(amount_total, 2)

	@api.depends('vatable_sales', 'vat_12', 'vat_exempt_sales', 'zero_rated_sales')
	def _compute_register_total(self):
		for r in self:
			r.register_total = round(
				r.vatable_sales + r.vat_12 + r.vat_exempt_sales + r.zero_rated_sales, 2)

	# PLEASE FIX THE METHOD BELOW, ONCE THE MODULE FOR PWD AND SC DISCOUNTS ARE COMPLETED
	# PLEASE ADD NEW FIELDS FOR FETCHING THE CORRESPONDING DISCOUNTS:
	# # # * SC/PWD 5%
	# # # * SC 20%
	# # # * PWD 20%

	@api.depends('total_discounts')
	def _fetch_regular_discount(self):
		for r in self:
			r.regular_discount = r.total_discounts

	def generate_report(self):
		data = {
			'date_start': self.start_date,
			'date_stop': self.end_date,
			'company_name': self.env.company.name,
			'total_sales': self.total_sales,
			'total_returns': self.total_returns,
			'total_voids': self.total_voids,
			'total_discounts': self.total_discounts,
			'subtotal': self.subtotal,
			'vatable_sales': self.vatable_sales,
			'vat_12': self.vat_12,
			'vat_exempt_sales': self.vat_exempt_sales,
			'zero_rated_sales': self.zero_rated_sales,
			'register_total': self.register_total,
			'regular_discount': self.regular_discount,
			'beginning_reading': self.beginning_reading,
			'ending_reading': self.ending_reading,
		}

		data.update(self.get_payments(
			data['date_start'], data['date_stop']))

		# change self to []; what's the difference?
		return self.env.ref('cc_z_reading.action_z_reading_report').report_action([], data=data) 

	"""
		below are for the z-reading views;
	"""
	def action_view_returns(self):
		sessions = self.is_available(
			self.start_date, self.end_date, self.crm_team_id)
		if sessions:
			domain = ['&', ['amount_total', '<', '0'],
				['session_id', '=', sessions.ids]]
		else:
			domain = []
		return {
			'name': _('Returns'),
			'res_model': 'pos.order',
			'view_mode': 'tree',
			'views': [
				(self.env.ref('cc_z_reading.z_reading_view_returns_tree').id, 'tree'),
				],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'domain': domain,
		}

	def action_view_sales(self):
		sessions = self.is_available(self.start_date,self.end_date,self.crm_team_id)

		if sessions:
			domain = [['session_id', 'in', sessions.ids]]
		else:
			domain = []
		return {
			'name': _('Sales'),
			'res_model': 'pos.order',
			'view_mode': 'tree',
			'views': [
				(self.env.ref('cc_z_reading.z_reading_view_sales_tree').id, 'tree'),
				],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'domain': domain,
		}

	"""
		for now this is commented out;
		once the void module is added, add this in the view;
	"""
	
	# def action_view_voids(self):
	#     sessions = self.is_available(self.start_date,self.end_date,self.crm_team_id)
	#     print("Session Id type > ", type(sessions.ids))
	#     if sessions:
	#         domain = [['session_id', 'in', sessions.ids]]
	#     else:
	#         domain = []
	#     return {
	#         'name': _('Sales'),
	#         'res_model': 'pos.order',
	#         'view_mode': 'tree',
	#         'views': [
	#             (self.env.ref('cc_z_reading.z_reading_view_sales_tree').id, 'tree'),
	#             ],
	#         'type': 'ir.actions.act_window',
	#         'target': 'new',
	#         'domain': domain,
	#     }

	def action_view_discounts(self):
		sessions = self.is_available(self.start_date,self.end_date,self.crm_team_id)

		if sessions:
			domain = [['session_id', 'in', sessions.ids]]
			orders = self.env['pos.order'].search(domain)
			domain = ["&",["order_id", 'in', orders.ids],["discount","!=",0]]
		else:
			domain = []
		return {
			'name': _('Discounts'),
			'res_model': 'pos.order.line',
			'view_mode': 'tree',
			'views': [
				(self.env.ref('cc_z_reading.z_reading_view_discounts_tree').id, 'tree'),
				],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'domain': domain,
		}

	def action_view_vat_sales(self):
		sessions = self.is_available(self.start_date,self.end_date,self.crm_team_id)

		if sessions:
			domain = [['session_id', 'in', sessions.ids]]
			orders = self.env['pos.order'].search(domain)
			domain = ["&",["order_id", 'in', orders.ids],["tax_ids.tax_type", "=", "vatable"]]
		else:
			domain = []
		return {
			'name': _('Vatable sales'),
			'res_model': 'pos.order.line',
			'view_mode': 'tree',
			'views': [
				(self.env.ref('cc_z_reading.z_reading_view_vat_sales_tree').id, 'tree'),
				],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'domain': domain,
		}

	def action_view_vat_12(self):
		sessions = self.is_available(self.start_date,self.end_date,self.crm_team_id)

		if sessions:
			domain = ["&",['session_id', 'in', sessions.ids],["lines.tax_ids.tax_type", "=", "vatable"]]
			
		else:
			domain = []
		return {
			'name': _('12% VAT'),
			'res_model': 'pos.order',
			'view_mode': 'tree',
			'views': [
				(self.env.ref('cc_z_reading.z_reading_view_vat_12_tree').id, 'tree'),
				],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'domain': domain,
		}

	def action_view_vat_exempt(self):
		sessions = self.is_available(self.start_date,self.end_date,self.crm_team_id)
		
		if sessions:
			domain = ["&",['session_id', 'in', sessions.ids],["lines.tax_ids.tax_type", "=", "vat_exempt"]]
			
		else:
			domain = []
		return {
			'name': _('VAT Exempt Sales'),
			'res_model': 'pos.order',
			'view_mode': 'tree',
			'views': [
				(self.env.ref('cc_z_reading.z_reading_view_vat_exempt_tree').id, 'tree'),
				],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'domain': domain,
		}

	def action_view_zero_rated(self):
		sessions = self.is_available(self.start_date,self.end_date,self.crm_team_id)

		if sessions:
			domain = ["&",['session_id', 'in', sessions.ids],["lines.tax_ids.tax_type", "=", "zero_rated"]]
			
		else:
			domain = []
		return {
			'name': _('VAT Exempt Sales'),
			'res_model': 'pos.order',
			'view_mode': 'tree',
			'views': [
				(self.env.ref('cc_z_reading.z_reading_view_zero_rated_tree').id, 'tree'),
				],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'domain': domain,
		}