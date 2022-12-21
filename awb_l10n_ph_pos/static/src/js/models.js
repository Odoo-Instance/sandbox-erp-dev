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
                vatable_sales = 0; //should exclude discount
                vat_amount = 0; //should exclude discount
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
                                // added computations for discount excluded vat amount and sales
                                var real_price_without_tax_total = orderlines[id].price_with_tax_before_discount / (1 + (tax_details[x].tax.amount / 100));
                                vat_amount += (orderlines[id].price_with_tax_before_discount - real_price_without_tax_total);
                                vatable_sales += real_price_without_tax_total;
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
            
            
            // match the crm_team_id of this session to this.pos.team.id
            // get the sales team's info 

            var this_crm_team_id = this.pos.config.crm_team_id;
            console.log("crm_team_id ", this_crm_team_id);

            var all_sales_team = this.pos.team;
            console.log("all sales team", all_sales_team);

            var min = "";
            var sn = "";
            var ptu = "";
            var remarks = "";

            for (var x = 0; x < all_sales_team.length; x++){
                if (all_sales_team[x].id == this_crm_team_id[0]){
                    min = all_sales_team[x].taxpayer_min;
                    sn = all_sales_team[x].taxpayer_machine_serial_number;
                    ptu = all_sales_team[x].awb_pos_provider_ptu;
                    remarks = all_sales_team[x].awb_pos_provider_remarks;

                    console.log("MIN > ", min);
                    console.log("SN > ", sn);
                    console.log("PTU > ", ptu);
                    console.log("Remarks > ", remarks);
                }
            }
            
            // VAT inclusive prices computations
            // variable initialization
            // remove unused variables later.
            var price_with_quantity_no_discount = 0;
            var price_with_quantity_no_discount_total = 0;
            
            var original_price_with_tax = 0;
            var original_price_with_tax_total = 0;
                    
            var discount_value = 0;
            
            var price_with_quantity_with_discount_w_tax = 0;
            var price_with_quantity_with_discount_total_w_tax = 0;
            
            var subtotal_tax_inclusive = 0;
            var custom_total_discount = 0;

            // for every orderline
            for(var x = 0; x < orderlines.length; x++){
                console.log("for orderlines", orderlines[x]);

                //compute the price of the orderline if there is a quantity but without discount
                //multiply the quantity to get the total
                price_with_quantity_no_discount = orderlines[x].price + (orderlines[x].tax / orderlines[x].quantity);
                price_with_quantity_no_discount_total = price_with_quantity_no_discount * orderlines[x].quantity;
                
                //for all taxes details
                //match the tax id to the groupTaxes, which is already arranged per orderlines
                //e.g. groupTaxes["9","8"] == orderlines["0", "1"] taxes
                //when matched, calculate the original price of the orderline with the tax amount
                //before the discount
                //removed because of tax inclusive
                // for (var y in tax_details) {
                //     if (tax_details[y].tax.id == groupTaxes[x]) {
                //         original_price_with_tax = (tax_details[y].tax.amount / 100 * orderlines[x].fixed_lst_price) + orderlines[x].fixed_lst_price;
                //         original_price_with_tax_total = original_price_with_tax * orderlines[x].quantity;
                
                //     }
                // }
                //get the discount value of the orderline with the tax.
                discount_value = orderlines[x].discount / 100 * orderlines[x].fixed_lst_price;
                custom_total_discount += discount_value; 
                // discount_value = (orderlines[x].discount / 100 * orderlines[x].fixed_lst_price) * orderlines[x].quantity;
                //get the price of the orderline with discount, with tax.
                price_with_quantity_with_discount_w_tax = orderlines[x].fixed_lst_price - (discount_value / orderlines[x].quantity);
                price_with_quantity_with_discount_total_w_tax = orderlines[x].fixed_lst_price - discount_value;
                //add to subtotal
                //nothings gonna show up if the product has no taxes that was tagged to it
                //since we are getting the summation from the price_with_quantity_with_discount_total_w_tax
                subtotal_tax_inclusive += price_with_quantity_with_discount_total_w_tax;
                //save all computations to the orderlines object for fetching
                //all should have .toFixed to prevent minor discrepancies
                orderlines[x].price_with_quantity_no_discount = price_with_quantity_no_discount.toFixed(2);
                orderlines[x].price_with_quantity_no_discount_total = price_with_quantity_no_discount_total.toFixed(2);
                
                // orderlines[x].original_price_with_tax = orderlines[x].fixed_lst_price.toFixed(2); // before discount
                // orderlines[x].original_price_with_tax_total = orderlines[x].fixed_lst_price_total.toFixed(2); // before discount
                
                orderlines[x].discount_value = discount_value.toFixed(2); // discount
                
                orderlines[x].price_with_quantity_with_discount_w_tax = price_with_quantity_with_discount_w_tax.toFixed(2); // after discount
                orderlines[x].price_with_quantity_with_discount_total_w_tax = price_with_quantity_with_discount_total_w_tax.toFixed(2); // after discount
            }

            var receipt = {
                receipt_number: this.pos.order.next_sequence_number, //display next receipt number
                zero_rated: zero_rated,
                vatable_sales: vatable_sales,
                vat_exempt: vat_exempt,
                vat_amount: vat_amount,
                orderlines: orderlines,
                paymentlines: paymentlines,
                custom_total_discount: custom_total_discount,
                subtotal_tax_inclusive: subtotal_tax_inclusive,
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
                machine_info: {
                    min: min,
                    sn: sn,
                    ptu: ptu,
                    remarks: remarks,
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
            console.log("custom_total_discount", custom_total_discount);
            return receipt;
        }
    });
});