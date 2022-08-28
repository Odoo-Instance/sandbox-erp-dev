$(document).ready(function(){

    $(document).on('change', '#total_grant_requested', function(event){
        if ($(event.target).val() != '' && $('#project_location').val() != '') {
            set_tier_values()
        }
    });

    function set_tier_values() {
        var value = $('#total_grant_requested').val();
        $('.grant_req_error_message').addClass('d-none');
        $('.grant_req_error_message').text('');
        $('.strategic_objective').addClass('d-none');
        $('div.strategic_objective_table').addClass('d-none');
        $('div.headline_output_table').addClass('d-none');
        if (parseFloat(value) <= parseFloat($('#tier_one').val())){
            $('#tier_value').val('Tier 1');
        }
        else if (parseFloat(value) <= parseFloat($('#tier_two').val())){
            $('#tier_value').val('Tier 2');
        }
        else {
            $('#tier_value').val('Tier 3');
            $('.strategic_objective').removeClass('d-none');
            $('div.headline_output_table').removeClass('d-none');
            $('div.strategic_objective_table').removeClass('d-none');
        }

        if (parseFloat(value) > parseFloat($('#tier_three').val())) {
            $('.grant_req_error_message').text('The maximum available Grant is £ ' + parseFloat($('#tier_three').val()));
            $('.grant_req_error_message').removeClass('d-none');
        }
    }

    $(document).on('change', '#post_code', function(event){
        var post_code_value = $(event.target).val();
        var grant_types = $('select[name="grant_types_id"]').val();
        if (grant_types != '' && post_code_value != ''){
            $.ajax({
                url : "/get/project_location/",
                data: {
                    'grant_type': grant_types,
                    'post_code_value': post_code_value
                },
                type: 'POST',
            })
            .then(function(result){
                result = JSON.parse(result);
                if (result) {
                    $('#project_location').val(result.location_id);
                    $('#project_location').change();
                }
            });
        }
    });

    $(document).on('change', '#project_id', function(event){
        var project_id = $(event.target).val();
        $('.project_not_found_error').addClass('d-none');
        if (project_id != ''){
            $.ajax({
                url : "/get/project/",
                data: {
                    'project_id': project_id,
                },
                type: 'POST',
            })
            .then(function(result){
                result = JSON.parse(result);
                if (result) {
                    if (result.project_name != '' && result.project_name !== undefined) {
                    }
                    else {
                        $('.project_not_found_error').removeClass('d-none');
                    }
                }
            });
        }
    });

    $(document).on('keyup', '.strategic_text', function(event){
        var words = 0;
        if ((this.value.match(/\S+/g)) != null) {
            words = this.value.match(/\S+/g).length;
        }
        if (words > 200) {
            // Split the string on first 200 words and rejoin on spaces
            var trimmed = $(this).val().split(/\s+/, 200).join(" ");
            // Add a space at the end to make sure more typing creates new words
            $(this).val(trimmed + " ");
        }
    });

    $(document).on('click', '.is_strategic', function(event){
        var is_strategic = $(event.target).prop('checked')
        var textarea = $(event.target).parent().next().find('textarea');
        if (is_strategic && $(textarea).attr('disabled') !== undefined) {
            $(textarea).removeAttr('disabled');
        }
        else {
            $(textarea).attr('disabled', 'disabled');
        }
    });

    $(document).on('click', '.is_headline', function(event){
        var is_headline = $(event.target).prop('checked')
        var input = $(event.target).parent().next().find('input');
        if (is_headline && $(input).attr('disabled') !== undefined) {
            $(input).removeAttr('disabled');
        }
        else {
            $(input).attr('disabled', 'disabled');
        }
    });

    $(document).on('click', '.application_submit', function(event){
        var rows = $('.total_project_costs > tbody > tr.project_cost_line');
        $('.strategic_objective_error_message').addClass('d-none')
        $('.headline_outputs_error_message').addClass('d-none')
        var cost_data = [];
        _.each(rows, function(row) {
            let expenditure = $(row).find('input[name="expenditure"]').val();
            let total_cost = $(row).find('input[name="total_cost"]').val();
            cost_data.push({
                'expenditure': expenditure,
                'total_cost': total_cost,
            });
        });
        if ($('#tier_value').val() == 'Tier 3') {
            var strategic_rows = $('.strategic_objective_table > tbody > tr.new_strategic_line');
            var strategic_ticked_rows = strategic_rows.find('input[name="is_strategic"]:checked');
            if (strategic_ticked_rows.length == 0) {
                $('.strategic_objective_error_message').removeClass('d-none');
                return false;
            }
            var headline_rows = $('.headline_output_table > tbody > tr.new_headline_line');
            var headline_ticked_rows = headline_rows.find('input[name="is_headline"]:checked');
            if (headline_ticked_rows.length == 0) {
                $('.headline_outputs_error_message').removeClass('d-none');
                return false;
            }
            
            var strategic_data = [];
            _.each(strategic_ticked_rows, function(row) {
                var parent_line = $(row).parent().parent();
                let name = $(parent_line).find('input[name="strategic_name"]').val();
                let is_strategic = $(parent_line).find('input[name="is_strategic"]').prop('checked');
                let strategic_text = $(parent_line).find('textarea[name="strategic_text"]').val();
                strategic_data.push({
                    'name': name,
                    'is_strategic': is_strategic,
                    'strategic_text': strategic_text,
                });
            });
            $('textarea[name="strategic_objective_ids"]').val(JSON.stringify(strategic_data));
            
            var headline_data = [];
            _.each(headline_ticked_rows, function(row) {
                var parent_line = $(row).parent().parent();
                let name = $(parent_line).find('input[name="headline_name"]').val();
                let is_headline = $(parent_line).find('input[name="is_headline"]').prop('checked');
                let headline_text = $(parent_line).find('input[name="headline_text"]').val();
                headline_data.push({
                    'name': name,
                    'is_headline': is_headline,
                    'headline_text': headline_text,
                });
            });
            $('textarea[name="headline_outputs_ids"]').val(JSON.stringify(headline_data));
        }
        else {
            $('textarea[name="strategic_objective_ids"]').remove();
            $('textarea[name="headline_outputs_ids"]').remove();
        }

        $('textarea[name="project_cost_ids"]').val(JSON.stringify(cost_data));
        if ($('.error:not(.d-none)').length == 0) {
            $('.form_submit').click();
        }
    });

    $(document).on('change', '.total_cost', function(event){
        var rows = $('.total_project_costs > tbody > tr.project_cost_line').find('input[name="total_cost"]');
        var cost = 0;
        _.each(rows, function(element) {
            if ($(element).val() != '') {
                cost += parseFloat($(element).val());
            }
        });
        $('#total_line_cost').val(cost);
    });

    $(document).on('change', '.total_cost, #total_grant_requested', function(event){
        if (parseFloat($('#total_grant_requested').val()) < 1000 || (parseFloat($('#total_line_cost').val()) > 0 && parseFloat($('#total_grant_requested').val()) != '' && parseFloat($('#total_line_cost').val()) < parseFloat($('#total_grant_requested').val()))){
            $('.another_grant_req_error_message').text('Grant must be more than £1000 and less than Project Cost');
            $('.another_grant_req_error_message').removeClass('d-none');
        }
        else {
            $('.another_grant_req_error_message').addClass('d-none');
        }
    });

    $(document).on('change', '#project_location', function(event){
        var grant_types = $('select[name="grant_types_id"]').val();
        var project_location = $(event.target).val();
        if (grant_types != '' && project_location != ''){
            $.ajax({
                url : "/get/grant_type/",
                data: {
                    'grant_type': grant_types,
                    'location': project_location
                },
                type: 'POST',
            })
            .then(function(result){
                result = JSON.parse(result);
                if (result) {
                    $('#tier_one').val(result.tier_one);
                    $('#tier_two').val(result.tier_two);
                    $('#tier_three').val(result.tier_three);
                    if ($('#total_grant_requested').val() != '') {
                        set_tier_values()
                    }
                    $('.new_strategic_line').remove();
                    add_strategic_lines(result.strategic_data);
                    $('.new_headline_line').remove();
                    add_headline_lines(result.headline_data)
                }
            });
        }
    });

    function add_strategic_lines(data) {
        _.each(data, function(line){
            var $new_row = $('.add_extra_strategic').clone(true);
            $new_row.removeClass('d-none');
            $new_row.removeClass('add_extra_strategic');
            $new_row.addClass('new_strategic_line');
            $new_row.insertBefore($('.add_extra_strategic'));
            $new_row.find('input[name="strategic_name"]').val(line.name);
        });
    }
    function add_headline_lines(data) {
        _.each(data, function(line){
            var $new_row = $('.add_extra_headline').clone(true);
            $new_row.removeClass('d-none');
            $new_row.removeClass('add_extra_headline');
            $new_row.addClass('new_headline_line');
            $new_row.insertBefore($('.add_extra_headline'));
            $new_row.find('input[name="headline_name"]').val(line.name);
        });
    }

    $(".is_previous_project").change(function(){
        $('.project_not_found_error').addClass('d-none');
        $('#project_id').val('');
        if($(this).prop("checked")){
            $(".project").removeClass('d-none');
            $(".project_details").removeClass('d-none');
            $("#project_id").attr('required', 'required');
        }
        else{
            $(".project").addClass('d-none');
            $(".project_details").addClass('d-none');
            $("#project_id").removeAttr('required');
        }
    });
    
    $(document).on('change', '#planned_start_date', function(event){
        var current_date = moment().format('YYYY-MM-DD');
        var planned_date = $(event.target).val();
        var future_date = moment().add('weeks', 6).format('YYYY-MM-DD');
        $('.previous_start_date_error').addClass('d-none');
        $('.future_date_error').addClass('d-none');
        if (planned_date < current_date) {
            $('.previous_start_date_error').removeClass('d-none');
        }
        else if (current_date <= planned_date && future_date >= planned_date) {
            $('.future_date_error').text('Please note that a grant application approval could take up to 6 weeks.');
            $('.future_date_error').removeClass('d-none');
        }
    });

    $(document).on('change', '#planned_start_date, #planned_end_date', function(event){
        var start_date = $('#planned_start_date').val();
        var end_date = $('#planned_end_date').val();
        $('.end_date_error').addClass('d-none');
        if (end_date < start_date) {
            $('.end_date_error').removeClass('d-none');
        }
    });
    
    $(".add_total_project").click(function (){
        var $new_row = $('.add_extra_project').clone(true);
        $new_row.removeClass('d-none');
        $new_row.removeClass('add_extra_project');
        $new_row.addClass('project_cost_line');
        $new_row.insertBefore($('.add_extra_project'));
        _.each($new_row.find('td'), function(val) {
            $(val).find('input').attr('required', 'required');
        });
    });

    $(document).on('click', '.remove_line', function() {
        $(this).parent().parent().remove();
        $('.total_cost').trigger('change');
    });

  
});