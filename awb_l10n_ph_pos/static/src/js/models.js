odoo.define('awb_l10n_ph_pos.models', function (require) {
    'use strict';

    const { Context } = owl;
    var models = require('point_of_sale.models');
    var core = require('web.core');

    var _t = core._t;
    var _super_order = models.Order.prototype;

    var OrderlineCollection = Backbone.Collection.extend({
        model: _super_order.Orderline,
    });

    var PaymentlineCollection = Backbone.Collection.extend({
        model: _super_order.Paymentline,
    });

    // load fields from res.company that was not previously loaded on the parent
    // class for getting the full address of the taxpayer

    models.load_fields('res.company', [
        'street',
        'street2',
        'city',
        'state_id',
        'zip',
    ]
    );

    // load fields from account.tax to get the tax_type of the product
    models.load_fields('account.tax', [
        'tax_type',
    ]);

    // extend the order class to alter the function mentioned below;
    // calculations for the vat/non-vat related info were added for the printing of the receipt;
    // later on, create a model to save the vat info in the database and
    // do the calculation in the python models;

    models.Order = models.Order.extend({
        // An order more or less represents the content of a client's shopping cart (the OrderLines)
        // plus the associated payment information (the Paymentlines)
        // there is always an active ('selected') order in the Pos, a new one is created
        // automaticaly once an order is completed and sent to the server.
        initialize: function (attributes, options) {
            _super_order.initialize.apply(this, arguments);
            var self = this;
            options = options || {};

            this.locked = false;
            this.pos = options.pos;
            this.selected_orderline = undefined;
            this.selected_paymentline = undefined;
            this.screen_data = {};  // see Gui
            this.temporary = options.temporary || false;
            this.creation_date = new Date();
            this.to_invoice = false;
            this.orderlines = new OrderlineCollection();
            this.paymentlines = new PaymentlineCollection();
            this.pos_session_id = this.pos.pos_session.id;
            this.employee = this.pos.employee;
            this.finalized = false; // if true, cannot be modified.
            this.set_pricelist(this.pos.default_pricelist);

            this.set({ client: null });

            this.uiState = {
                ReceiptScreen: new Context({
                    inputEmail: '',
                    // if null: not yet tried to send
                    // if false/true: tried sending email
                    emailSuccessful: null,
                    emailNotice: '',
                }),
                TipScreen: new Context({
                    inputTipAmount: '',
                })
            };

            // FETCH taxpayer_receipt
            var receipt_type = this.pos.company.taxpayer_receipt.toUpperCase();

            if (options.json) {
                this.init_from_JSON(options.json);
            } else {
                this.sequence_number = this.pos.pos_session.sequence_number++;
                this.uid = this.generate_unique_id();
                this.name = _.str.sprintf(_t("%s # %s"), receipt_type, this.uid); //add receipt type as prefix
                this.validation_date = undefined;
                this.fiscal_position = _.find(this.pos.fiscal_positions, function (fp) {
                    return fp.id === self.pos.config.default_fiscal_position_id[0];
                });
            }

            this.on('change', function () { this.save_to_db("order:change"); }, this);
            this.orderlines.on('change', function () { this.save_to_db("orderline:change"); }, this);
            this.orderlines.on('add', function () { this.save_to_db("orderline:add"); }, this);
            this.orderlines.on('remove', function () { this.save_to_db("orderline:remove"); }, this);
            this.paymentlines.on('change', function () { this.save_to_db("paymentline:change"); }, this);
            this.paymentlines.on('add', function () { this.save_to_db("paymentline:add"); }, this);
            this.paymentlines.on('remove', function () { this.save_to_db("paymentline:rem"); }, this);

            if (this.pos.config.iface_customer_facing_display) {
                this.paymentlines.on('add', this.pos.send_current_order_to_customer_facing_display, this.pos);
                this.paymentlines.on('remove', this.pos.send_current_order_to_customer_facing_display, this.pos);
            }

            this.save_to_db();

            return this;
        },
        save_to_db: function () {
            if (!this.temporary && !this.locked) {
                this.assert_editable();
                this.pos.db.save_unpaid_order(this);
            }
        },
        /**
         * Initialize PoS order from a JSON string.
         *
         * If the order was created in another session, the sequence number should be changed so it doesn't conflict
         * with orders in the current session.
         * Else, the sequence number of the session should follow on the sequence number of the loaded order.
         *
         * @param {object} json JSON representing one PoS order.
         */
        init_from_JSON: function (json) {
            _super_order.init_from_JSON.apply(this, arguments);

            var client;
            if (json.state && ['done', 'invoiced', 'paid'].includes(json.state)) {
                this.sequence_number = json.sequence_number;
            } else if (json.pos_session_id !== this.pos.pos_session.id) {
                this.sequence_number = this.pos.pos_session.sequence_number++;
            } else {
                this.sequence_number = json.sequence_number;
                this.pos.pos_session.sequence_number = Math.max(this.sequence_number + 1, this.pos.pos_session.sequence_number);
            }
            this.session_id = this.pos.pos_session.id;
            this.uid = json.uid;

            // FETCH taxpayer_receipt
            var receipt_type = this.pos.company.taxpayer_receipt.toUpperCase();

            this.name = _.str.sprintf(_t("%s # %s"), receipt_type, this.uid); //add receipt type as prefix
            this.validation_date = json.creation_date;
            this.server_id = json.server_id ? json.server_id : false;
            this.user_id = json.user_id;

            if (json.fiscal_position_id) {
                var fiscal_position = _.find(this.pos.fiscal_positions, function (fp) {
                    return fp.id === json.fiscal_position_id;
                });

                if (fiscal_position) {
                    this.fiscal_position = fiscal_position;
                } else {
                    console.error('ERROR: trying to load a fiscal position not available in the pos');
                }
            }

            if (json.pricelist_id) {
                this.pricelist = _.find(this.pos.pricelists, function (pricelist) {
                    return pricelist.id === json.pricelist_id;
                });
            } else {
                this.pricelist = this.pos.default_pricelist;
            }

            if (json.partner_id) {
                client = this.pos.db.get_partner_by_id(json.partner_id);
                if (!client) {
                    console.error('ERROR: trying to load a partner not available in the pos');
                }
            } else {
                client = null;
            }
            this.set_client(client);

            this.temporary = false;     // FIXME
            this.to_invoice = false;    // FIXME
            this.to_ship = false;

            var orderlines = json.lines;
            for (var i = 0; i < orderlines.length; i++) {
                var orderline = orderlines[i][2];
                if (this.pos.db.get_product_by_id(orderline.product_id)) {
                    this.add_orderline(new models.Orderline({}, { pos: this.pos, order: this, json: orderline }));
                }
            }

            var paymentlines = json.statement_ids;
            for (var i = 0; i < paymentlines.length; i++) {
                var paymentline = paymentlines[i][2];
                var newpaymentline = new models.Paymentline({}, { pos: this.pos, order: this, json: paymentline });
                this.paymentlines.add(newpaymentline);

                if (i === paymentlines.length - 1) {
                    this.select_paymentline(newpaymentline);
                }
            }

            // Tag this order as 'locked' if it is already paid.
            this.locked = ['paid', 'done', 'invoiced'].includes(json.state);
            this.state = json.state;
            this.amount_return = json.amount_return;
            this.account_move = json.account_move;
            this.backendId = json.id;
            this.isFromClosedSession = json.is_session_closed;
            this.is_tipped = json.is_tipped || false;
            this.tip_amount = json.tip_amount || 0;


        },
        export_for_printing: function () {

            var orderlines = [];
            var self = this;

            this.orderlines.each(function (orderline) {
                orderlines.push(orderline.export_for_printing());
            });

            // If order is locked (paid), the 'change' is saved as negative payment,
            // and is flagged with is_change = true. A receipt that is printed first
            // time doesn't show this negative payment so we filter it out.
            var paymentlines = this.paymentlines.models
                .filter(function (paymentline) {
                    return !paymentline.is_change;
                })
                .map(function (paymentline) {
                    return paymentline.export_for_printing();
                });
            var client = this.get('client');
            var cashier = this.pos.get_cashier();
            var company = this.pos.company;
            var date = new Date();

            function is_html(subreceipt) {
                return subreceipt ? (subreceipt.split('\n')[0].indexOf('<!DOCTYPE QWEB') >= 0) : false;
            }

            function render_html(subreceipt) {
                if (!is_html(subreceipt)) {
                    return subreceipt;
                } else {
                    subreceipt = subreceipt.split('\n').slice(1).join('\n');
                    var qweb = new QWeb2.Engine();
                    qweb.debug = config.isDebug();
                    qweb.default_dict = _.clone(QWeb.default_dict);
                    qweb.add_template('<templates><t t-name="subreceipt">' + subreceipt + '</t></templates>');

                    return qweb.render('subreceipt', { 'pos': self.pos, 'order': self, 'receipt': receipt });
                }
            }

            //the following are used for fetching the sales per receipt/invoice type
            //later have it be saved to the database
            var vatable_sales = 0;
            var vat_amount = 0;
            var zero_rated = 0;
            var vat_exempt = 0;
            var groupTaxes = [];
            var tax_details = this.get_tax_details();

            this.orderlines.each(function (line) {
                vatable_sales = 0;
                vat_amount = 0;
                zero_rated = 0;
                vat_exempt = 0;

                var taxDetails = line.get_tax_details();

                // 1. from groupTaxes, use the id and find the tax_type in tax_details
                // 2. if tax_type == etc. get price_without_tax as sales

                var taxIds = Object.keys(taxDetails);

                for (var t = 0; t < taxIds.length; t++) {
                    var taxId = taxIds[t];

                    groupTaxes.push(taxId);
                }

                for (var id = 0; id < groupTaxes.length; id++) {
                    for (var x in tax_details) {
                        if (groupTaxes[id] == tax_details[x].tax.id) {
                            var tax_type = tax_details[x].tax.tax_type;

                            if (tax_type == "zero_rated") {
                                zero_rated += orderlines[id].price_without_tax;
                            }
                            else if (tax_type == "vatable") {
                                vat_amount += orderlines[id].tax;
                                vatable_sales += orderlines[id].price_without_tax;
                            }
                            else if (tax_type == "vat_exempt") {
                                vat_exempt += orderlines[id].price_without_tax;
                            }
                        }
                    }
                }
            });

            var address_array = [company.city, company.state_id[1], company.zip];
            var address_info = "";
            for (var x = 0; x < address_array.length; x++) {
                if (address_array[x] != null) {
                    address_info = address_info + " " + address_array[x];
                }
            }

            var receipt = {
                zero_rated: zero_rated,
                vatable_sales: vatable_sales,
                vat_exempt: vat_exempt,
                vat_amount: vat_amount,
                orderlines: orderlines,
                paymentlines: paymentlines,
                subtotal: this.get_subtotal(),
                total_with_tax: this.get_total_with_tax(),
                total_rounded: this.get_total_with_tax() + this.get_rounding_applied(),
                total_without_tax: this.get_total_without_tax(),
                total_tax: this.get_total_tax(),
                total_paid: this.get_total_paid(),
                total_discount: this.get_total_discount(),
                rounding_applied: this.get_rounding_applied(),
                tax_details: this.get_tax_details(),
                change: this.locked ? this.amount_return : this.get_change(),
                name: this.get_name(),
                client: client ? client : null,
                invoice_id: null,   //TODO
                cashier: cashier ? cashier.name : null,
                precision: {
                    price: 2,
                    money: 2,
                    quantity: 3,
                },
                date: {
                    year: date.getFullYear(),
                    month: date.getMonth(),
                    date: date.getDate(),       // day of the month
                    day: date.getDay(),         // day of the week
                    hour: date.getHours(),
                    minute: date.getMinutes(),
                    isostring: date.toISOString(),
                    localestring: this.formatted_validation_date,
                    validation_date: this.validation_date,
                },
                company: {
                    email: company.email,
                    website: company.website,
                    company_registry: company.company_registry,
                    street: company.street,
                    street2: company.street2,
                    address_info: address_info,
                    city: company.city,
                    state: company.state_id[1],
                    zip: company.zip,
                    country: company.country_id[1],
                    vat: company.vat,
                    vat_label: company.country && company.country.vat_label || _t('Tax ID'),
                    name: company.name,
                    phone: company.phone,
                    logo: this.pos.company_logo_base64,
                },
                currency: this.pos.currency,
            };

            if (is_html(this.pos.config.receipt_header)) {
                receipt.header = '';
                receipt.header_html = render_html(this.pos.config.receipt_header);
            } else {
                receipt.header = this.pos.config.receipt_header || '';
            }

            if (is_html(this.pos.config.receipt_footer)) {
                receipt.footer = '';
                receipt.footer_html = render_html(this.pos.config.receipt_footer);
            } else {
                receipt.footer = this.pos.config.receipt_footer || '';
            }
            if (!receipt.date.localestring && (!this.state || this.state == 'draft')) {
                receipt.date.localestring = field_utils.format.datetime(moment(new Date()), {}, { timezone: false });
            }

            return receipt;
        }
    });
});