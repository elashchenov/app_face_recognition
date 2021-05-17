# msg if some errors while updatig data in database param:(table, data, filter)
db_update_error = "Error when updating data (def update_database(self, table, data, filter)), the filter parameter is set incorrectly. (Input data: table = %s; data = %s; filter = %s)"


"""_______________________________________________________________
                            API(main.py)
   _______________________________________________________________"""

"""*********GET_INFO_ACTIONS*********"""

# msg for function get info action
get_info_action_log = "The get_info_action function was called"

"""*********INFO_USERS*********"""

# msg for function get info users help
get_info_users_help_log = "The info_user_help function was called"

# msg for function get info user with param(email:string)
get_info_users_log = "The info_user function is called with the parameter:%s"

"""*********ADD_REMOVAL_EQUIPMENT*********"""

# msg for function add removal equipment help info
add_removal_equipment_help_log = "The add_removal_equipment help function was called"

# msg for function add removal equipment
add_removal_equipment_log = "The add_removal_equipment function was called"

# error msg when input data in function add removal equipment is not valid (input_data:json)
error_add_removal_eqipmet_get_json_log = "Error when extracting input parameters from json format:%s"

"""*********ADD_REMOVAL_CHAIR*********"""

# msg for function add removal chair
add_removal_chair_log = "The add_removal_chair function was called"

# error msg when input data in function add removal chair is not valid (input_data:json)
error_add_removal_chair_get_json_log = "Error when extracting input parameters from json format:%s"

"""*********SEND_USER_NOTIFICATION*********"""

# msg for function send user notification with params (email:string, city:string, location:string)
send_user_notification_log = "The send_user_notification function was called. Params: %s, %s, %s"

"""*********CHECK_REMOVAL*********"""

# msg for function check removal with params (type:string, id:int)
check_removal_log = "The check_removal function was called. Params: %s, %s"

"""*********UPDATE_CHAIR_REQUEST*********"""

# msg for function update chair request with params (email:string, date_out:string, bc_name:string)
update_chair_request_log = "The update_chair_request function was called. Params: %s, %s, %s"

"""*********ADD_REMOVAL_EQUIPMENT_NEW_USERS*********"""

# msg for function add removal equipment 
add_removal_equipment_new_users_log = "The add_removal_equipment_new_users function was called"

# error msg when input data in function add removal equipment new users is not valid (input_data:json)
error_add_removal_eqipmet_new_users_get_json_log = "Error when extracting input parameters from json format:%s"

"""_______________________________________________________________"""


"""_______________________________________________________________
                            functions.py
   _______________________________________________________________"""

"""*********GET_INFO_EQUIPMENT*********"""

# error while get info from db about equipment(params: data-string)
error_get_inf_equip = "Error when executing a request to get equipment data. Input params: %s"

"""*********GET_INFO_EQUIPMENT*********"""

# error while get info from db about user(params: data-string)
error_get_inf_usr = "Error when executing a request to get user data. Input params: %s"

"""*********ADD_REMOVAL_EQUIPMENT*********"""

# msg when function add removal equipment started(params: email-string, equipment_data-list of dicts, date_take_out-string, bc_name-string)
msg_add_removal_equipment_input_log = "The function for the removal of equipment with input parameters is started: %s, %s, %s, %s"

"""*********REMOVAL_CHAIR*********"""

# msg when function removal chair started(params: email-string, date_out-string, bc_name-string)
msg_removal_chair_input_log = "The function for the removal chair with input parameters is started: %s, %s, %s"

"""*********SEND_EMAIL_USER*********"""

# msg when function send email user started(params: email-string, city-string, location-string)
msg_send_email_user_input_log = "The function send email user with input parameters is started: %s, %s, %s"

"""*********CHECK_REMOVAL*********"""

# msg when function check removal started(params: type-string, id-string)
msg_check_removal_input_log = "The function check removal with input parameters is started: %s, %s"

"""*********REPEAT_CHAIR_REQUEST*********"""

# msg when function repeat chair request started(params: bc_name-string, date_out-string, email-string)
msg_repeat_chair_request_input_log = "The function repeat chair request with input parameters is started: %s, %s, %s"

"""*********UPDATE_DATA_CHAIR*********"""

# msg when function update_data_chair started(params: email-string, date_out-string, bc_name-string)
msg_update_data_chair_input_log = "The function update data chair with input parameters is started: %s, %s, %s"

"""*********ADD_REMOVAL_EQUIPMENT_NEW_USERS*********"""

# msg when function add removal equipment for new users started(params: name-string, surname-string, partronymic-string, email-string, legal_entity-string, equipment_data-dict, date_take_out-string, bc_name-string)
msg_add_removal_equipment_new_users_input_log = "The function for the removal of equipment to new users with input parameters is started: %s, %s, %s, %s, %s, %s, %s, %s"

"""*********GET_FREE_EQUIPMENT*********"""

# msg when a user from the list of warehouse employees is not found in the database(params: email-string)
msg_empty_warehouse_user_log = "Warehouse employee not found in the database: %s"