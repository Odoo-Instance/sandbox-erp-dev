odoo.define('cc_application.form_submit', function(require){
    "use strict";
    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');

    publicWidget.registry.applicatonUploadForm = publicWidget.Widget.extend({
        selector: '#applicarion_sign_up_form_section',
        events: {
               'click .application_save': '_onChangeChild',
    },
    image_data: function() {
    return new Promise(function(resolve, reject) {
        var self = this;
        var image_input = '';
        if (document.getElementById('credit_check') != null){
        var file = document.getElementById('credit_check').files[0];
        if (file) {
             var reader = new FileReader();
             reader.readAsDataURL(file);
             reader.onload = function(e)

                 {
                     image_input = reader.result;
                     resolve(image_input);
                 }
           }
        }else {
                   resolve(image_input);

           }

        });
    },
     _onChangeChild: async function (ev) {
             var self = this;
             var credit_check_value = document.getElementById('credit_check').value;
             console.log('files',credit_check_value);
             if(credit_check_value){

                      var new_data = await self.image_data();
             }
            var your_name =$('#your_name').val();
            var email =$('#email').val();
            var phone =$('#phone').val();
            var position =$('#position').val();
            var secondary_contact_name =$('#contact_secondary_contact_name').val();
            var alter_phone =$('#alter_phone').val();
            var application_id = $('#application_id').val();
            var org_name = $('#org_name').val();
            var sic_code = $('#sic_code').val();
            var fte_count = $('#fte_count').val();
            var credit_check = new_data;
            var org_house_no = $('#org_house_no').val();
            var org_charity_no = $('#org_charity_no').val();
            var org_website = $('#org_website').val();
            var org_type = $('#org_type').val();
            var org_type_detail = $('#org_type_detail').val();
            var org_size = $('#org_size').val();
            var org_about = $('#org_about').val();
            var org_street = $('#org_street').val();
            var org_street2 = $('#org_street2').val();
            var org_city = $('#org_city').val();
            var org_state = $('#org_state').val();
            var org_zip = $('#org_zip').val();
            var org_country = $('#org_country').val();
            var alternative_address_sel = $('#alternative_address_sel').val();
            var alternative_street = $('#alternative_street').val();
            var alternative_street2 = $('#alternative_street2').val();
            var alternative_city = $('#alternative_city').val();
            var alternative_state = $('#alternative_state').val();
            var alternative_zip = $('#alternative_zip').val();
            var alternative_country = $('#alternative_country').val();
            var org_start_date = $('#org_start_date').val();
            var org_legal_status = $('#org_legal_status').val();
            var org_utr = $('#org_utr').val();
            var org_house_id = $('#org_house_id').val();
            var org_charity_id = $('#org_charity_id').val();
            var org_legal_about = $('#org_legal_about').val();
            var org_vat = $('#org_vat').val();
            var org_net_or_cost = $('#org_net_or_cost').val();
            var vat_reg_no = $('#vat_reg_no').val();
            var org_gross_about = $('#org_gross_about').val();
            var employee_male = $('#employee_male').val();
            var employee_female = $('#employee_female').val();
            var employee_gender_not_to_say = $('#employee_gender_not_to_say').val();
            var employee_disable = $('#employee_disable').val();
            var employee_not_disable = $('#employee_not_disable').val();
            var employee_disability_not_to_say = $('#employee_disability_not_to_say').val();
            var employee_16_24 = $('#employee_16_24').val();
            var employee_25_29 = $('#employee_25_29').val();
            var employee_30_34 = $('#employee_30_34').val();
            var employee_35_39 = $('#employee_35_39').val();
            var employee_40_45 = $('#employee_40_45').val();
            var employee_45_49 = $('#employee_45_49').val();
            var employee_50_54 = $('#employee_50_54').val();
            var employee_55_59 = $('#employee_55_59').val();
            var employee_60_64 = $('#employee_60_64').val();
            var employee_65 = $('#employee_65').val();
            var employee_age_not_to_say = $('#employee_age_not_to_say').val();
            var employee_white = $('#employee_white').val();
            var employee_mixed = $('#employee_mixed').val();
            var employee_multiple_ethnic_groups = $('#employee_multiple_ethnic_groups').val();
            var employee_asian_british = $('#employee_asian_british').val();
            var employee_asian = $('#employee_asian').val();
            var employee_black = $('#employee_black').val();
            var employee_african = $('#employee_african').val();
            var employee_caribbean = $('#employee_caribbean').val();
            var employee_black_british = $('#employee_black_british').val();
            var employee_other_ethnic_group = $('#employee_other_ethnic_group').val();
            var employee_cat_not_to_say = $('#employee_cat_not_to_say').val();
            var org_employee_fte = $('#org_employee_fte').val();
            var rows = $('.org_share_holders_table_1 > tbody > tr.org_share_holders_table_line');
                    var share_holder_details_ids = [];
                    _.each(rows, function(row) {
                        let share_holder_name = $(row).find('input[name="share_holder_name"]').val();
                        let company_reg_no = $(row).find('input[name="company_reg_no"]').val();
                        let share_in_percent = $(row).find('input[name="share_in_percentage"]').val();
                        let no_of_employees = $(row).find('input[name="no_of_employees"]').val();
                        let comment = $(row).find('input[name="comment"]').val();
                        console.log(share_in_percent,'share1');
                        share_holder_details_ids.push({
                            'share_holder_name': share_holder_name,
                            'company_reg_no': company_reg_no,
                            'share_in_percentage': share_in_percent,
                            'no_of_employees': no_of_employees,
                            'comment': comment
                        });
                        console.log('share_holder_details_ids',share_holder_details_ids);
                    });
            var rows = $('.share_holder_table > tbody > tr.share_holder_table_line');
                    var business_share_details_ids = [];
                    _.each(rows, function(row) {
                        let share_holder_name = $(row).find('input[name="share_holder_name"]').val();
                        let company_reg_no = $(row).find('input[name="company_reg_no"]').val();
                        let share_in_percent = $(row).find('input[name="share_in_percentage"]').val();
                        let no_of_employees = $(row).find('input[name="no_of_employees"]').val();
                        let comment = $(row).find('input[name="comment"]').val();
                        console.log(share_in_percent,'share');
                        business_share_details_ids.push({
                            'share_holder_name': share_holder_name,
                            'company_reg_no': company_reg_no,
                            'share_in_percentage': share_in_percent,
                            'no_of_employees': no_of_employees,
                            'comment': comment
                        });
                        console.log('business_share_details_ids',business_share_details_ids);

                    });

            var rows = $('.share_holder_details_table > tbody > tr.share_holder_details_table_line');
                    var share_holder_ids = [];
                    _.each(rows, function(row) {
                        let share_holder_name = $(row).find('input[name="share_holder_name"]').val();
                        let share_in_percent = $(row).find('input[name="share_in_percentage"]').val();
                        let comment = $(row).find('input[name="comment"]').val();
                        share_holder_ids.push({
                            'share_holder_name': share_holder_name,
                            'share_in_percentage': share_in_percent,
                            'comment': comment
                        });
                    });
             ajax.jsonRpc('/application/save/', 'call', {
                'credit_check': new_data,
                'your_name':your_name,
                'position':position,
                'email':email,
                'credit_check':'image_input',
                'phone':phone,
                'secondary_contact_name':secondary_contact_name,
                'alter_phone':alter_phone,
                'share_holder_details_ids':share_holder_details_ids,
                'share_holder_ids':share_holder_ids,
                'business_share_details_ids':business_share_details_ids,
                'sic_code':sic_code,
                'credit_check':credit_check,
                'application_id' : application_id,
                'org_name' : org_name,
                'org_website' : org_website,
                'org_type' : org_type,
                'org_type_detail' : org_type_detail,
                'org_size' : org_size,
                'org_about' : org_about,
                'org_address' : org_street,
                'org_start_date' : org_start_date,
                'org_legal_status' : org_legal_status,
                'org_utr' : org_utr,
                'org_house_id' : org_house_id,
                'org_charity_id' : org_charity_id,
                'org_legal_about' : org_legal_about,
                'org_vat' : org_vat,
                'org_net_or_cost' : org_net_or_cost,
                'vat_reg_no' : vat_reg_no,
                'org_gross_about' : org_gross_about,
                'employee_male' : employee_male,
                'employee_female' : employee_female,
                'employee_gender_not_to_say' : employee_gender_not_to_say,
                'employee_disable' : employee_disable,
                'employee_not_disable' : employee_not_disable,
                'employee_disability_not_to_say' : employee_disability_not_to_say,
                'employee_16_24' : employee_16_24,
                'employee_25_29' : employee_25_29,
                'employee_30_34' : employee_30_34,
                'employee_35_39' : employee_35_39,
                'employee_40_45' : employee_40_45,
                'employee_45_49' : employee_45_49,
                'employee_50_54' : employee_50_54,
                'employee_55_59' : employee_55_59,
                'employee_60_64' : employee_60_64,
                'employee_65' : employee_65,
                'employee_age_not_to_say' : employee_age_not_to_say,
                'employee_white' : employee_white,
                'employee_mixed' : employee_mixed,
                'employee_multiple_ethnic_groups' : employee_multiple_ethnic_groups,
                'employee_asian_british' : employee_asian_british,
                'employee_asian' : employee_asian,
                'employee_black' : employee_black,
                'employee_african' : employee_african,
                'employee_caribbean' : employee_caribbean,
                'employee_black_british' : employee_black_british,
                'employee_other_ethnic_group' : employee_other_ethnic_group,
                'employee_cat_not_to_say' : employee_cat_not_to_say,
                'street':org_street,
                'street2':org_street2,
                'city':org_city,
                'state_id':org_state,
                'zip':org_zip,
                'country_id':org_country,
                'alternative_street':alternative_street,
                'alternative_street2':alternative_street2,
                'alternative_city':alternative_city,
                'alternative_state_id':alternative_state,
                'alternative_zip':alternative_zip,
                'alternative_country_id':alternative_country,
                'alternative_address_sel':alternative_address_sel
                   })
     }
    });


});