odoo.define('awb_l10n_ph_pos.OrderRecieptPosProvider', function (require) {
    'use strict'
    const models = require('point_of_sale.models');
    models.load_fields('res.company',
        ['taxpayer_info',
            'taxpayer_is_vat_registered',
            'taxpayer_remarks',
            'awb_pos_provider_id',
            'awb_pos_provider_tin',
            'awb_pos_provider_accreditation_no',
            'awb_pos_provider_display_date',
            'awb_pos_provider_display_valid_until',
            'awb_pos_provider_display_address',]);
    models.load_models([
        {
            //add domain to simplify the code in model.js
            model: 'crm.team',
            fields: [
                'taxpayer_min',
                'taxpayer_machine_serial_number',
                'awb_pos_provider_ptu',
                'awb_pos_provider_remarks',
                'current_sequence_number',
                'ending_sequence_number',
                'sale_team_prefix_id',
            ],
            domain: function(self){return [['id','=', self.config.crm_team_id[0]]];},
            loaded: function(self,data){
                self.team = data;
            }
        },
        ]);

    models.load_models([
        {
            model: 'pos.order',
            fields: ['next_sequence_number'], //removed pos_reference because it is not used
            domain: function(self){return [['crm_team_id.id','=', self.config.crm_team_id[0]]];},
            loaded: function(self,data){
                //if data is null or undefined, the next transaction will be the first of that
                //sales team; therefore, set self.order to first
                if (data.length == 0) {
                    //get current_sequence_number
                    //add 1
                    //zfill 6 
                    //check if pow(9,6)
                    //if true
                        //get length of ending_sequence_number.toString
                        //zfill current_sequence_number to length_ending_sequence_number
                    //take crm_team.sale_team_prefix_id.name + ' ' + current_sequence_number

                    var current_sequence_number = self.team[0].current_sequence_number;
                    var ending_sequence_number = self.team[0].ending_sequence_number;
                    var sale_team_prefix = self.team[0].sale_team_prefix_id[1];
                    var final_sequence_number = "";

                    current_sequence_number++;
                    current_sequence_number = current_sequence_number.toString();
                    while (current_sequence_number.length < 6){
                        current_sequence_number = "0" + current_sequence_number;
                    }
                    
                    if(ending_sequence_number > Math.pow(9,6)){
                        var length_of_ending_sequence_number = (length_of_ending_sequence_number.toString()).length;
                        while (current_sequence_number.length < length_of_ending_sequence_number){
                            current_sequence_number = "0" + current_sequence_number;
                        }
                    }

                    final_sequence_number = sale_team_prefix + ' ' + current_sequence_number;
                    
                    self.order = {
                        next_sequence_number: final_sequence_number,
                    }; //move to last
                    
                    console.log("final_sequence_number", final_sequence_number);
                    console.log("current_sequence_number", current_sequence_number);
                    console.log("Data empty. Created new sequence.");
                }
                else {
                    self.order = data[0];
                }
                debugger;
            }
        },
    ]);
});