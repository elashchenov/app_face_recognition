import os 

dir_source = "src"
path_to_token = os.path.join(dir_source, "token.txt")

host_api_db = "http://localhost"
port_api_db = "5050"

api_post_device = f'{host_api_db}:{port_api_db}/database/1.0.0/add-device/'
api_post_user = f'{host_api_db}:{port_api_db}/database/1.0.0/add-user'
api_check_user = f'{host_api_db}:{port_api_db}/database/1.0.0/check-user/'
api_get_access = f'{host_api_db}:{port_api_db}/database/1.0.0/login'
api_update_user_info = f'{host_api_db}:{port_api_db}/database/1.0.0/update-user'
api_add_photo = f'{host_api_db}:{port_api_db}/database/1.0.0/add-photo'
api_get_status_train = f'{host_api_db}:{port_api_db}/database/1.0.0/get-status-train'
api_add_journal = f'{host_api_db}:{port_api_db}/database/1.0.0/add-journal'

api_get_model = "http://localhost:5000/1.0.0/neural-network/get-model"
api_train_model = "http://localhost:5000/1.0.0/neural-network/train-model"
api_face_verify = "http://localhost:5000/1.0.0/neural-network/face-verify"


dict_user_info = {
    'name': None,
    'surname': None,
    'username': None,
    'email': None,
    'password': None,
    'device_id': None,
    'id_user': None
}

dict_login = {
    "login" : None,
    "password" : None
}