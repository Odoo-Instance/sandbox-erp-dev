$(document).ready(function(){

    function legalStatusChange(){
        var selectedValue = $('#org_legal_status').val();
        if (selectedValue=='sole_trader'){
            $("#sole_trader_view").css('display','flex');
            $("#org_comp_char_view").css('display','none');
            $("#org_other_view").css('display','none');
        }else if (selectedValue == 'partnership'){
            $("#sole_trader_view").css('display','flex');
            $("#org_comp_char_view").css('display','none');
            $("#org_other_view").css('display','none');
        }else if (selectedValue == 'company_ltd_by_shares' || selectedValue == 'company_ltd_by_guarantee' || selectedValue == 'community_interest_company' || selectedValue == 'limited_liability_partnership'){
            $("#sole_trader_view").css('display','none');
            $("#org_comp_char_view").css('display','flex');
            $("#org_comp_view").css('display','flex');
            $("#org_char_view").css('display','none');
            $("#org_other_view").css('display','none');
        }else if (selectedValue == 'other'){
            $("#sole_trader_view").css('display','none');
            $("#org_comp_char_view").css('display','none');
            $("#org_other_view").css('display','flex');
        }else if (selectedValue == 'registered_charity'){
            $("#sole_trader_view").css('display','none');
            $("#org_comp_char_view").css('display','flex');
            $("#org_comp_view").css('display','flex');
            $("#org_char_view").css('display','flex');
            $("#org_other_view").css('display','none');
        }
        else{
            console.log('null');
        }
    }
    legalStatusChange();
    $('input[type=radio][name=alternative_address_sel]').change(function() {
        if (this.value == 'i_have') {
            $("#alternative_street").css('visibility','visible');
            $("#alternative_street2").css('visibility','visible');
            $("#alternative_city").css('visibility','visible');
            $("#alternative_state").css('visibility','visible');
//            $('#alternative_state').prop('selectedIndex',0);
            $("#alternative_zip").css('visibility','visible');
            $("#alternative_country").css('visibility','visible');
//            $('#alternative_country').prop('selectedIndex',0);
        }else if (this.value == 'i_dont_have') {
            $("#alternative_street").val('');
            $("#alternative_street").css('visibility','hidden');
            $("#alternative_street2").val('');
            $("#alternative_street2").css('visibility','hidden');
            $("#alternative_city").val('');
            $("#alternative_city").css('visibility','hidden');
//            $('#alternative_state').prop('selectedIndex',0);
            $("#alternative_state").css('visibility','hidden');
            $("#alternative_zip").val('');
            $("#alternative_zip").css('visibility','hidden');
//            $('#alternative_country').prop('selectedIndex',0);
            $("#alternative_country").css('visibility','hidden');
        }
    });

    $("#org_legal_status").change(function(){
        legalStatusChange();
     });
     $("#org_utr").keyup(function(){
        var UtrValue = $(event.target).val();
        if (UtrValue.length > 10) {
            $('#org_utr_error').removeClass('d-none');

        }
        else if (UtrValue.length < 10) {
            $('#org_utr_error').addClass('d-none');
        }
     });
     $("#org_about").keyup(function(){
        var AboutValue = $(event.target).val();
        if (AboutValue.trim().split(" ").length > 200) {
            $('#org_about_business_error').removeClass('d-none');

        }
        else if (AboutValue.trim().split(" ").length < 200) {
            console.log('kjh');
            $('#org_about_business_error').addClass('d-none');
        }
     });

    $('input[type=radio][name=org_vat]').change(function() {
        if (this.value == 'registered') {
            $("#org_net_gross").css('display','block');
            $("#org_vat_no_view").css('display','block');

        }else if (this.value == 'not_registered') {
            $("#org_net_gross").css('display','none');
            $("#org_vat_no_view").css('display','none');
            $("#org_gross_reason").css('display','none');
        }
    });

    $('input[type=radio][name=link_org]').change(function() {
        if (this.value == 'yes') {
            $("#link_org_no_view").css('display','block');

        }else if (this.value == 'no') {
            $("#link_org_no_view").css('display','none');
        }
    });
    $('input[type=radio][name=is_prev_funding]').change(function() {
        if (this.value == 'yes') {
            $("#previous_funding").css('display','block');

        }else if (this.value == 'no') {
            $("#previous_funding").css('display','none');
        }
    });
    $('input[type=radio][name=is_dq_director]').change(function() {
        if (this.value == 'yes') {
            $("#dq_director_desc").css('display','block');

        }else if (this.value == 'no') {
            $("#dq_director_desc").css('display','none');
        }
    });
    $('input[type=radio][name=is_listed]').change(function() {
        if (this.value == 'yes') {
            $("#listed_desc").css('display','block');

        }else if (this.value == 'no') {
            $("#listed_desc").css('display','none');
        }
    });
    $('input[type=radio][name=is_subject_bankruptcy]').change(function() {
        if (this.value == 'yes') {
            $("#subject_bankruptcy_desc").css('display','block');

        }else if (this.value == 'no') {
            $("#subject_bankruptcy_desc").css('display','none');
        }
    });
    $('input[type=radio][name=is_subject_county]').change(function() {
        if (this.value == 'yes') {
            $("#subject_county_desc").css('display','block');

        }else if (this.value == 'no') {
            $("#subject_county_desc").css('display','none');
        }
    });
    $('input[type=radio][name=is_time_critical]').change(function() {
        if (this.value == 'yes') {
            $("#time_critical").css('display','block');

        }else if (this.value == 'no') {
            $("#time_critical").css('display','none');
        }
    });
    $('input[type=radio][name=org_net_or_cost]').change(function() {
        if (this.value == 'gross') {
            $("#vat_gross_eligibility_div").css('display','block');
        }else if (this.value == 'net') {
            $("#vat_gross_eligibility_div").css('display','none');
        }
    });


    $('input[type=radio][name=net_or_cost]').change(function() {
        if (this.value == 'net') {
            $("#org_gross_reason").css('display','none');
        }else if (this.value == 'gross') {
            $("#org_gross_reason").css('display','block');
        }
    });

    $("#org_type").change(function(ev){
        var selectedValue = $(ev.target[ev.target.selectedIndex]).data('name');
        console.log(selectedValue,'hhh');
        if (selectedValue === 'Other'){
            $("#org_type_detail_view").css('display','block');
        }else{
            $("#org_type_detail_view").css('display','none');
        }
    });

    $("#org_project_location").change(function(ev){
        var select = document.getElementById('org_project_location');
        var value = select.options[select.selectedIndex].value;
        if (value == '1'){
            console.log(value,'St Ives'); 
            $("#st_ives_no_view").css('display','block');
            $("#penzance_no_view").css('display','none');
        }else if (value == '2'){
            console.log(value,'Penzance'); 
            $("#penzance_no_view").css('display','block');
            $("#st_ives_no_view").css('display','none');
        }else{
            console.log(value,'3'); 
        }
    });


    $('input[type=radio][name=org_share_holders]').change(function() {
        if (this.value == 'no') {
            $("#share_holders_view").css('display','none');
        }else if (this.value == 'yes') {
            $("#share_holders_view").css('display','block');
        }
    });



    $('input[type=radio][name=org_share_holders1]').change(function() {
        if (this.value == 'no') {
            $("#org_share_holders_view1").css('display','none');
        }else if (this.value == 'yes') {
            $("#org_share_holders_view1").css('display','block');
        }
    });

});
//        image_data: function() {
//            return new Promise(function(resolve, reject) {
//            var self = this;
//            var image_input = '';
//            if (document.getElementById('logo_id') != null){
//            var file = document.getElementById('credit_check').files[0];
//            if (file) {
//                 var reader = new FileReader();
//                 reader.readAsDataURL(file);
//                 reader.onload = function(e)
//
//                     {
//                         image_input = reader.result;
//                         resolve(image_input);
//                     }
//               }
//            }else {
//                       resolve(image_input);
//
//               }
//
//            });
//    },
//


//    $('.application_save').on('click', function(){
//            if (document.getElementById('credit_check') != null){
//            var file = document.getElementById('credit_check').files[0];
//            console.log(file,"ftuuuuuuuuuuuuuuuuu")
//            if (file) {
//                 var reader = new FileReader();
//                 reader.readAsDataURL(file);
//                         console.log(reader.result,"hjkygyug")
//
//                 reader.onload = function(e)
//
//                     {
//                         var image_input = reader.result;
//                         console.log(image_input,"hhhhhhhhhhhhhh")
//                     }
//               }
//               }
//        var your_name =$('#your_name').val();
//        var email =$('#email').val();
//        var phone =$('#phone').val();
//        var position =$('#position').val();
//        var contact_secondary_contact_name =$('#contact_secondary_contact_name').val();
//        var alter_phone =$('#alter_phone').val();
//        var application_id = $('#application_id').val();
//        var org_name = $('#org_name').val();
//        var sic_code = $('#sic_code').val();
//        var fte_count = $('#fte_count').val();
////        var credit_check = $('#credit_check').files[0];
//        var org_house_no = $('#org_house_no').val();
//        var org_charity_no = $('#org_charity_no').val();
//        var org_website = $('#org_website').val();
//        var org_type = $('#org_type').val();
//        var org_type_detail = $('#org_type_detail').val();
//        var org_size = $('#org_size').val();
//        var org_about = $('#org_about').val();
//        var org_street = $('#org_street').val();
//        var org_street2 = $('#org_street2').val();
//        var org_city = $('#org_city').val();
//        var org_state = $('#org_state').val();
//        var org_zip = $('#org_zip').val();
//        var org_country = $('#org_country').val();
//        var alternative_address = $('#alternative_address').val();
//        var alternative_street = $('#alternative_street').val();
//        var alternative_street2 = $('#alternative_street2').val();
//        var alternative_city = $('#alternative_city').val();
//        var alternative_city = $('#alternative_city').val();
//        var alternative_state = $('#alternative_state').val();
//        var alternative_zip = $('#alternative_zip').val();
//        var alternative_country = $('#alternative_country').val();
//        var org_start_date = $('#org_start_date').val();
//        var org_legal_status = $('#org_legal_status').val();
//        var org_utr = $('#org_utr').val();
//        var org_house_id = $('#org_house_id').val();
//        var org_charity_id = $('#org_charity_id').val();
//        var org_legal_about = $('#org_legal_about').val();
//        var org_vat = $('#org_vat').val();
//        var org_net_or_cost = $('#org_net_or_cost').val();
//        var vat_reg_no = $('#vat_reg_no').val();
//        var org_gross_about = $('#org_gross_about').val();
//        var employee_male = $('#employee_male').val();
//        var employee_female = $('#employee_female').val();
//        var employee_gender_not_to_say = $('#employee_gender_not_to_say').val();
//        var employee_disable = $('#employee_disable').val();
//        var employee_not_disable = $('#employee_not_disable').val();
//        var employee_disability_not_to_say = $('#employee_disability_not_to_say').val();
//        var employee_16_24 = $('#employee_16_24').val();
//        var employee_25_29 = $('#employee_25_29').val();
//        var employee_30_34 = $('#employee_30_34').val();
//        var employee_35_39 = $('#employee_35_39').val();
//        var employee_40_45 = $('#employee_40_45').val();
//        var employee_45_49 = $('#employee_45_49').val();
//        var employee_50_54 = $('#employee_50_54').val();
//        var employee_55_59 = $('#employee_55_59').val();
//        var employee_60_64 = $('#employee_60_64').val();
//        var employee_65 = $('#employee_65').val();
//        var employee_age_not_to_say = $('#employee_age_not_to_say').val();
//        var employee_white = $('#employee_white').val();
//        var employee_mixed = $('#employee_mixed').val();
//        var employee_multiple_ethnic_groups = $('#employee_multiple_ethnic_groups').val();
//        var employee_asian_british = $('#employee_asian_british').val();
//        var employee_asian = $('#employee_asian').val();
//        var employee_black = $('#employee_black').val();
//        var employee_african = $('#employee_african').val();
//        var employee_caribbean = $('#employee_caribbean').val();
//        var employee_black_british = $('#employee_black_british').val();
//        var employee_other_ethnic_group = $('#employee_other_ethnic_group').val();
//        var employee_cat_not_to_say = $('#employee_cat_not_to_say').val();
//        var org_employee_fte = $('#org_employee_fte').val();
//        var org_address=org_street
//        var org_alternative_address_data=org_street.concat(" ",org_street2," ",org_city);
//        var rows = $('.org_share_holders_table_1 > tbody > tr.org_share_holders_table_line');
//                var share_holder_details_ids = [];
//                _.each(rows, function(row) {
//                    let share_holder_name = $(row).find('input[name="share_holder_name"]').val();
//                    let company_reg_no = $(row).find('input[name="company_reg_no"]').val();
//                    let share_in_percent = $(row).find('input[name="share_in_percentage"]').val();
//                    let no_of_employees = $(row).find('input[name="no_of_employees"]').val();
//                    let comment = $(row).find('input[name="comment"]').val();
//                    share_holder_details_ids.push({
//                        'share_holder_name': share_holder_name,
//                        'company_reg_no': company_reg_no,
//                        'share_in_percentage': share_in_percentage,
//                        'no_of_employees': no_of_employees,
//                        'comment': comment
//                    });
//                });
//        var rows = $('.share_holder_table > tbody > tr.share_holder_table_line');
//                var business_share_details_ids = [];
//                _.each(rows, function(row) {
//                    let share_holder_name = $(row).find('input[name="share_holder_name"]').val();
//                    let company_reg_no = $(row).find('input[name="company_reg_no"]').val();
//                    let share_in_percent = $(row).find('input[name="share_in_percentage"]').val();
//                    let no_of_employees = $(row).find('input[name="no_of_employees"]').val();
//                    let comment = $(row).find('input[name="comment"]').val();
//                    console.log(share_holder_name,comment);
//                    business_share_details_ids.push({
//                        'share_holder_name': share_holder_name,
//                        'company_reg_no': company_reg_no,
//                        'share_in_percentage': share_in_percentage,
//                        'no_of_employees': no_of_employees,
//                        'comment': comment
//                    });
//                });
//
//        var rows = $('.share_holder_details_table > tbody > tr.share_holder_details_table_line');
//                var share_holder_ids = [];
//                _.each(rows, function(row) {
//                    let share_holder_name = $(row).find('input[name="share_holder_name"]').val();
//                    let share_in_percent = $(row).find('input[name="share_in_percentage"]').val();
//                    let comment = $(row).find('input[name="comment"]').val();
//                    share_holder_ids.push({
//                        'share_holder_name': share_holder_name,
//                        'share_in_percentage': share_in_percentage,
//                        'comment': comment
//                    });
//                });
//        console.log(image_input,"ccccccccccccccccccccccccc")
//        $.ajax({ url : '/application/save/',
//            type: 'post',
//            contentType: 'Application/json',
//            dataType: 'Application/json',
//            data:JSON.stringify({
//                'your_name':your_name,
//                'position':position,
//                'email':email,
//                'credit_check':image_input,
//                'phone':phone,
//                'contact_secondary_contact_name':contact_secondary_contact_name,
//                'alter_phone':alter_phone,
//                'share_holder_details_ids':share_holder_details_ids,
//                'share_holder_ids':share_holder_ids,
//                'business_share_details_ids':business_share_details_ids,
//                'sic_code':sic_code,
//                'credit_check':credit_check,
//                'application_id' : application_id,
//                'org_name' : org_name,
//                'org_website' : org_website,
//                'org_type' : org_type,
//                'org_type_detail' : org_type_detail,
//                'org_size' : org_size,
//                'org_about' : org_about,
//                'org_address' : org_street,
//                'org_start_date' : org_start_date,
//                'org_legal_status' : org_legal_status,
//                'org_address' : org_address,
//                'org_alternative_address_data' : org_alternative_address_data,
//                'org_utr' : org_utr,
//                'org_house_id' : org_house_id,
//                'org_charity_id' : org_charity_id,
//                'org_legal_about' : org_legal_about,
//                'org_vat' : org_vat,
//                'org_net_or_cost' : org_net_or_cost,
//                'vat_reg_no' : vat_reg_no,
//                'org_gross_about' : org_gross_about,
//                'employee_male' : employee_male,
//                'employee_female' : employee_female,
//                'employee_gender_not_to_say' : employee_gender_not_to_say,
//                'employee_disable' : employee_disable,
//                'employee_not_disable' : employee_not_disable,
//                'employee_disability_not_to_say' : employee_disability_not_to_say,
//                'employee_16_24' : employee_16_24,
//                'employee_25_29' : employee_25_29,
//                'employee_30_34' : employee_30_34,
//                'employee_35_39' : employee_35_39,
//                'employee_40_45' : employee_40_45,
//                'employee_45_49' : employee_45_49,
//                'employee_50_54' : employee_50_54,
//                'employee_55_59' : employee_55_59,
//                'employee_60_64' : employee_60_64,
//                'employee_65' : employee_65,
//                'employee_age_not_to_say' : employee_age_not_to_say,
//                'employee_white' : employee_white,
//                'employee_mixed' : employee_mixed,
//                'employee_multiple_ethnic_groups' : employee_multiple_ethnic_groups,
//                'employee_asian_british' : employee_asian_british,
//                'employee_asian' : employee_asian,
//                'employee_black' : employee_black,
//                'employee_african' : employee_african,
//                'employee_caribbean' : employee_caribbean,
//                'employee_black_british' : employee_black_british,
//                'employee_other_ethnic_group' : employee_other_ethnic_group,
//                'employee_cat_not_to_say' : employee_cat_not_to_say
//            })
//         });
//    });

        $(document).on('click', '.share_remove_line', function() {
        $(this).parent().parent().remove();
    });

      $(document).on('click', '.share_holder_remove_line', function() {
        $(this).parent().parent().remove();
    });

    $(document).on('click', '.share_holder_details_remove_line', function() {
        $(this).parent().parent().remove();
    });

    $(document).on('click', '.subsidy_control_details_table_remove_line', function() {
        console.log('tested4');
        $(this).parent().parent().remove();
    });

     $(".add_org_share_holder_line").click(function (){
        console.log('tested');
        var $new_row = $('.add_extra_org_share_holders_table_line').clone(true);
        $new_row.removeClass('d-none');
        $new_row.removeClass('add_extra_org_share_holders_table_line');
        $new_row.addClass('org_share_holders_table_line');
        $new_row.insertBefore($('.add_extra_org_share_holders_table_line'));
        _.each($new_row.find('td'), function(val) {
            $(val).find('input').attr('required', 'required');
            });
        });

     $(".add_share_holder_line").click(function (){
        console.log('tested2');
        var $new_row = $('.add_extra_share_holder_table_line').clone(true);
        $new_row.removeClass('d-none');
        $new_row.removeClass('add_extra_share_holder_table_line');
        $new_row.addClass('share_holder_table_line');
        $new_row.insertBefore($('.add_extra_share_holder_table_line'));
        _.each($new_row.find('td'), function(val) {
            $(val).find('input').attr('required', 'required');
            });
        });

      $(".add_share_holder_details_line").click(function (){
        console.log('tested3');
        var $new_row = $('.add_extra_share_holder_details_table_line').clone(true);
        $new_row.removeClass('d-none');
        $new_row.removeClass('add_extra_share_holder_details_table_line');
        $new_row.addClass('share_holder_details_table_line');
        $new_row.insertBefore($('.add_extra_share_holder_details_table_line'));
        _.each($new_row.find('td'), function(val) {
            $(val).find('input').attr('required', 'required');
            });
        });

        $(".add_subsidy_control_details_line").click(function (){
          console.log('tested4');
          var $new_row = $('.add_extra_subsidy_control_details_line').clone(true);
          $new_row.removeClass('d-none');
          $new_row.removeClass('add_extra_subsidy_control_details_line');
          $new_row.addClass('subsidy_control_details_line');
          $new_row.insertBefore($('.add_extra_subsidy_control_details_line'));
          _.each($new_row.find('td'), function(val) {
              $(val).find('input').attr('required', 'required');
              });
          });
        
        $(".add_risk_details_line").click(function (){
            console.log('tested');
            var $new_row = $('.add_extra_risk_table_line').clone(true);
            $new_row.removeClass('d-none');
            $new_row.removeClass('add_extra_risk_table_line');
            $new_row.addClass('risk_table_line');
            $new_row.insertBefore($('.add_extra_risk_table_line'));
            _.each($new_row.find('td'), function(val) {
                $(val).find('input').attr('required', 'required');
                });
            });

        $(".add_milestone_details_line").click(function (){
            console.log('tested');
            var $new_row = $('.add_extra_milestone_table_line').clone(true);
            $new_row.removeClass('d-none');
            $new_row.removeClass('add_extra_milestone_table_line');
            $new_row.addClass('milestone_table_line');
            $new_row.insertBefore($('.add_extra_milestone_table_line'));
            _.each($new_row.find('td'), function(val) {
                $(val).find('input').attr('required', 'required');
                });
            });
        
        $(".form_milestone_date").change(function(){
        	console.log('logger');
            var start_date = $('#planned_start_date').val();
            var end_date = $('#planned_end_date').val();
            var milestone_date = $('#milestone_date').val();
            $('.date_between_start_end').addClass('d-none');
            if (milestone_date < start_date || milestone_date > end_date) {
                $('.date_between_start_end').removeClass('d-none');
            }
        });
        
//        $(document).on('change','#planned_start_date,#planned_end_date,#milestone_date',function(event){
//        	console.log('logger');
//            var start_date = $('#planned_start_date').val();
//            var end_date = $('#planned_end_date').val();
//            var milestone_date = $('#milestone_date').val();
//            $('.date_between_start_end').addClass('d-none');
//            if (milestone_date < start_date || milestone_date > end_date) {
//                $('.date_between_start_end').removeClass('d-none');
//            }
//        });
//        $(document).on('change','#planned_start_date,#planned_end_date,#practical_date',function(event){
//        	console.log('logger');
//            var start_date = $('#planned_start_date').val();
//            var end_date = $('#planned_end_date').val();
//            var practical_date = $('#practical_date').val();
//            $('.date_between_start_end2').addClass('d-none');
//            if (practical_date < start_date || practical_date > end_date) {
//                $('.date_between_start_end2').removeClass('d-none');
//            }
//        });
        
        $(".form_practical_date").change(function(){
        	console.log('logger');
            var start_date = $('#planned_start_date').val();
            var end_date = $('#planned_end_date').val();
            var practical_date = $('#practical_date').val();
            $('.date_between_start_end2').addClass('d-none');
            if (practical_date < start_date || practical_date > end_date) {
                $('.date_between_start_end2').removeClass('d-none');
            }
        });
        
