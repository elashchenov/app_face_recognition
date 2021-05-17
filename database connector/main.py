import json

import flask
from flask import request
from waitress import serve
import ast
import config.config as conf
import src.action_processor as act_proccessor
from config.links import *
from config.log_msg import *
from src.exception import PrintException
from src.logger import get_logger
import base64
import os

logger = get_logger()
app = flask.Flask(__name__)
act_proc = act_proccessor.ActionProcessor()

"""_______________________________________________________________
    Function need to convert data to json
    Input:
        1. data to be converted to json - any
    Output: 
        data in json
    _______________________________________________________________"""


def to_json(data):
    return json.dumps(data, ensure_ascii=False) + "\n"


"""_______________________________________________________________
    Function need to configure output response
    Input:
        1. API status number-int
        2. The returned data-any
    Output: 
        flask.Response
    _______________________________________________________________"""


def resp(code, data):
    return flask.Response(
        status=code,
        response=data
    )


"""_______________________________________________________________
    Function need to configure base path response
    Input:
        None
    Output: 
        base path response - flask.redirect
    _______________________________________________________________"""


@app.route('/')
def root():
    return flask.redirect(main_link)


"""_______________________________________________________________
    Function need to response error page not found
    Input:
        None
    Output: 
        error response - flask.Response
    _______________________________________________________________"""


@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


"""_______________________________________________________________
    Function need to print error in log file
    Input:
        1. flag exception, need when use block try before-boolean
    Output: 
        error response - flask.Response
    _______________________________________________________________"""


def response_error_invalid_data(flag):
    if flag:
        logger.error(PrintException())
    return resp(405, "")


"""_______________________________________________________________
    Function is required to get reference information about the 
    API
    Input:
        None
    Output: 
        response with API info - flask.Response
    _______________________________________________________________"""


@app.route(check_user, methods=['GET'])
def _check_user_(email):
    # logger.info(get_info_action_log)
    return resp(200, act_proc.check_user(email))


@app.route(add_device, methods=['POST'])
def _add_device_(device_name):
    # logger.info(get_info_action_log)
    return resp(200, act_proc.add_device(device_name))



"""_______________________________________________________________
    Function is necessary to get information about the user
    Input:
        1. user email - string
    Output: 
        response with info - flask.Response
    _______________________________________________________________"""


@app.route(delete_user, methods=['GET'])
def _delete_user_(email):
    # logger.info(get_info_users_log % email)
    return resp(200, act_proc.delete_user(email))



"""_______________________________________________________________
    Function that is required to call the function add removal 
    equipment
    Input:
        1. Json data with param:
            a. email - string
            b. equipment_data - list of dict with item:
                i. equipment_number - string
                ii. service_number - string
            c. date_take_out - string date in format dd.mm.yyyy
            d. bc_name - string
    Output: 
        response with info - flask.Response
    _______________________________________________________________"""


@app.route(add_user, methods=['POST'])
def _add_user_():
    # logger.info(add_removal_equipment_log)
    json_data = request.get_json(force=True)
    user_data = {}
    try:
        logger.info(json_data)
        user_data = {
            'name': json_data["name"],
            'surname':json_data["surname"],
            'username':json_data["username"],
            'email':json_data["email"].lower(),
            'password':base64.b64decode(json_data["password"]).decode(),
            'device_id':json_data["device_id"]
        }
    except Exception as e:
        logger.error(e)
        # logger.error(error_add_removal_eqipmet_get_json_log % json_data)
        return resp(400, "ERROR")
    return resp(200, act_proc.add_user(user_data))

@app.route(update_user, methods=['POST'])
def _update_user_():
    # logger.info(add_removal_equipment_log)
    json_data = request.get_json(force=True)
    user_data = {}
    try:
        logger.info(json_data)
        user_data = {
            'id': json_data["id_user"],
            'name': json_data["name"],
            'surname':json_data["surname"],
            'username':json_data["username"],
            'email':json_data["email"].lower(),
            'password': base64.b64decode(json_data["password"]).decode()
        }
    except Exception as e:
        logger.error(e)
        # logger.error(error_add_removal_eqipmet_get_json_log % json_data)
        return resp(400, "ERROR")
    return resp(200, act_proc.update_user(user_data))

@app.route(login, methods=['GET'])
def _login_():
    # logger.info(add_removal_equipment_log)
    json_data = request.get_json(force=True)
    user_data = {}
    try:
        logger.info(json_data)
        user_data = {
            'email': json_data["email"],
            'password':base64.b64decode(json_data["password"]).decode()
        }
    except Exception as e:
        logger.error(e)
        # logger.error(error_add_removal_eqipmet_get_json_log % json_data)
        return resp(400, "ERROR")

    return resp(200, to_json(act_proc.login(user_data)))

@app.route(get_status_train, methods=['GET'])
def _get_status_train_():
    # logger.info(add_removal_equipment_log)
    json_data = request.get_json(force=True)
    user_data = {}
    try:
        logger.info(json_data)
        user_data = {
            'id_user': json_data["id_user"]
        }
    except Exception as e:
        logger.error(e)
        # logger.error(error_add_removal_eqipmet_get_json_log % json_data)
        return resp(400, "ERROR")
    return resp(200, to_json(act_proc.get_status_train(user_data)))

@app.route(add_photo, methods=['POST'])
def _add_photo_():
    # logger.info(add_removal_equipment_log)
    json_data = request.get_json(force=True)
    photo_data = {}
    # logger.info(json_data[1])
    try:
        # logger.info(json_data[1])
        photo_data = {
            'user_id': int(json_data[0]),
            'image':base64.b64decode(json_data[1]).decode()
        }
        # logger.info(type(ast.literal_eval(photo_data["image"])))
        # # image = open(os.path.join(conf.work_path, 'img', 'img1.png'), 'wb')
        # # image.write(str.encode(photo_data["image"]))
        # # image.close()
    except Exception as e:
        logger.error(e)
        # logger.error(error_add_removal_eqipmet_get_json_log % json_data)
        return resp(400, "ERROR")
    return resp(200, to_json(act_proc.add_photo(photo_data)))

@app.route(set_percent, methods=['POST'])
def _set_percent_(percent, id_user):
    return resp(200, to_json(act_proc.set_percent(percent, id_user)))


@app.route(add_item_journal, methods=['POST'])
def _add_journal_():
    # logger.info(add_removal_equipment_log)
    json_data = request.get_json(force=True)
    user_data = {}
    try:
        logger.info(json_data)
        user_data = {
            'user_id': int(json_data["id_user"])
        }
    except Exception as e:
        logger.error(e)
        # logger.error(error_add_removal_eqipmet_get_json_log % json_data)
        return resp(400, "ERROR")
    return resp(200, act_proc.add_item_to_journal(user_data['user_id']))


"""In furture version
    Function for returning equipment to the office"""
# @app.route(delete_removal_equipment, methods=['POST'])
# def _delete_removal_equipment_():
#     json_data = request.get_json(force=True)
#     try:
#         email = json_data["email"].lower()
#         equipment_number = json_data["equipment_number"]
#         date_return = json_data["date_return"]
#     except:
#         return resp(400, "ERROR")
#     return resp(200, to_json(func.delete_removal_equipment(email, equipment_number, date_return)))


# """_______________________________________________________________
#     Function that is required to call the function add removal 
#     chair
#     Input:
#         1. Json data with param:
#             a. email - string
#             b. date_take_out - string date in format dd.mm.yyyy
#             c. bc_name - string
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(add_removal_chair, methods=['POST'])
# def _add_removal_chair_():
#     logger.info(add_removal_chair_log)
#     json_data = request.get_json(force=True)
#     try:
#         email = json_data["email"].lower()
#         date_take_out = json_data["date_take_out"]
#         bc_name = json_data["bc_name"]
#     except:
#         logger.error(error_add_removal_chair_get_json_log % json_data)
#         return resp(400, "ERROR")
#     return resp(200, to_json(func.removal_chair(email, date_take_out, bc_name)))


# """_______________________________________________________________
#     Function that is required to call the function send user
#     notification
#     Input:
#         1. email - string
#         2. city - string
#         3. location - string
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(send_user_notification, methods=['GET'])
# def _send_user_notification_(email, city, location):
#     logger.info(send_user_notification_log % (email, city, location))
#     return resp(200, func.send_email_user(email.lower(), city, location))


# """_______________________________________________________________
#     Function that is required to call the function check removal
#     Input:
#         1. type - string, available value:
#             a. equipment
#             b. chair
#         2. id - int (id in database)
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(check_removal, methods=['GET'])
# def _check_removal_(type, id):
#     logger.info(check_removal_log % (type, id))
#     return resp(200, func.check_removal(type, id))


# """_______________________________________________________________
#     Function that is required to call the function update chair
#     request
#     Input:
#         1. email - string
#         2. date_out - string data in format dd.mm.yyyy
#         3. bc_name - string
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(update_chair_request, methods=['GET'])
# def _update_data_chair_(email, date_out, bc_name):
#     logger.info(update_chair_request_log % (email, date_out, bc_name))
#     return resp(200, func.update_data_chair(email, date_out, bc_name))


# """_______________________________________________________________
#     Function that is required to call the function date_of_uploads
#     Input:
#         None
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(date_uploads, methods=['GET'])
# def _date_uploads_():
#     return resp(200, func.get_date_of_upload())


# """_______________________________________________________________
#     Function that is required to call the function add removal 
#     equipment for new users
#     Input:
#         1. Json data with param:
#             a. name - string
#             b. surname - string
#             c. partronymic - string
#             d. email - string
#             e. legal_entity - string
#             b. equipment_data - list of dict with item:
#                 i. number - string
#                 ii. name - string
#             c. date_take_out - string date in format dd.mm.yyyy
#             d. bc_name - string
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(add_removal_equipment_new_user, methods=['POST'])
# def _add_removal_equipment_new_users_():
#     logger.info(add_removal_equipment_new_users_log)
#     json_data = request.get_json(force=True)
#     try:
#         name = json_data["name"]
#         surname = json_data["surname"]
#         partronymic = json_data["partronymic"]
#         email = json_data["email"].lower()
#         legal_entity = json_data["legal_entity"]
#         equipment_data = json_data["equipment_data"]
#         date_take_out = json_data["date_take_out"]
#         bc_name = json_data["bc_name"]
#     except:
#         logger.error(
#             error_add_removal_eqipmet_new_users_get_json_log % json_data)
#         return resp(400, "ERROR")
#     return resp(200, to_json(func.add_removal_equipment_new_users(name, surname, partronymic, email, legal_entity, equipment_data, date_take_out, bc_name)))

# """_______________________________________________________________
#     Function that is required to call the function get_free_equipment
#     Input:
#         None
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(get_equipment, methods=['GET'])
# def _get_equipment_(equipment_number):
#     return resp(200, to_json(func.get_equipment_by_equipmnet_num(equipment_number)))

# """_______________________________________________________________
#     Function that is required to call the function get_equipment
#     Input:
#         equipment_number - string
#     Output: 
#         response with info - flask.Response
#     _______________________________________________________________"""


# @app.route(get_free_equipment, methods=['GET'])
# def _get_free_equipment_():
#     return resp(200, to_json(func.get_free_equipment()))

if __name__ == "__main__":
    app.debug = True
    serve(app, host=conf.host, port=conf.port)
