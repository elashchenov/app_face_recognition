from waitress import serve
import config.config as conf
import base64
import requests
import pytest
import threading
import json
import os

import main
from src.database import DatabaseConnector
from src.logger import get_logger


def run_flask_app():
    app = main.app
    serve(app, host=conf.host, port=conf.port)


t = threading.Thread(target=run_flask_app)
t.start()

host_api_db = "http://localhost"
port_api_db = "5050"

device_name = '3d81f5f9-fd2c062153-6d390e'

database = DatabaseConnector(conf.db_name, get_logger())


class TestDB():

    def test_add_device(self):
        """Добавление устройства в базу данных"""
        response = requests.post(f"{host_api_db}:{port_api_db}/database/1.0.0/add-device/{device_name}")
        dev_id = database.select('device', 'id', f'name = \'{device_name}\'')
        assert len(dev_id)
        assert response.content == b'success'

    def test_add_new_user(self):
        """Пользователь успешно добавляется в базу данных"""
        dict_user = {
            'name': 'pytest_user',
            'surname': 'pytest_user',
            'username': 'pytest_user',
            'email': 'pytest_user@gmail.com',
            'password': base64.b64encode(bytes('123456', "utf-8")).decode('ascii'),
            'device_id': device_name
        }
        response = requests.post(f'{host_api_db}:{port_api_db}/database/1.0.0/add-user', json=dict_user)

        user_id = database.select('users', 'id', f'email = \'{dict_user["email"]}\'')
        assert len(user_id)
        assert response.content == b'success'

        # row_for_delete = [{'id': user_id}]
        # database.delete('users', row_for_delete)

    def test_add_existing_user(self):
        """Существующий пользователь пытается добавится в БД"""
        dict_user = {
            'name': 'pytest_user',
            'surname': 'pytest_user',
            'username': 'pytest_user',
            'email': 'pytest_user@gmail.com',
            'password': base64.b64encode(bytes('123456', "utf-8")).decode('ascii'),
            'device_id': device_name
        }
        response = requests.post(f'{host_api_db}:{port_api_db}/database/1.0.0/add-user', json=dict_user)

        assert response.content == b'exists'

    def test_login(self):
        """Успешная авторизация при правильных учетных данных"""
        dict_login = {
            'email': 'pytest_user@gmail.com',
            'password': base64.b64encode(bytes(str('123456'), "utf-8")).decode('ascii')
        }
        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/login', json=dict_login)
        response_data = json.loads(response.content)
        assert response_data[0] == 'success'

        user_id = database.select('users', 'id', f'email = \'{dict_login["email"]}\'')
        assert str(user_id[0][0]) == response_data[1][0]

    def test_wrong_login(self):
        """Авторизация при неправильных учетных данных"""
        """Успешная авторизация при правильных учетных данных"""
        dict_login = {
            'email': 'pytest_user@gmail.com',
            'password': base64.b64encode(bytes(str('123456afklasjdf'), "utf-8")).decode('ascii')
        }
        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/login', json=dict_login)
        response_data = json.loads(response.content)
        assert response_data[0] == 'error'


    def test_train_status(self):
        """Успешное получение статуса обучения модели для пользователя"""
        user_email = 'pytest_user@gmail.com'
        user_id = database.select('users', 'id', f'email = \'{user_email}\'')[0][0]

        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/get-status-train',
                                json={'id_user': user_id})

        assert response.content != b'"error"\n'

    def test_update_train_status(self):
        """Успешное обновление статуса обучения модели"""
        user_email = 'pytest_user@gmail.com'
        user_id = database.select('users', 'id', f'email = \'{user_email}\'')[0][0]
        database.update('users', {"percent_train": int(float(0))}, f'id = {user_id}')
        percent = database.select('users', 'percent_train', f'email = \'{user_email}\'')[0][0]
        assert percent == 0

        response = requests.post(f'{host_api_db}:{port_api_db}/database/1.0.0/set-percent/'
                      + '99' + "/" + str(user_id))

        assert response.content == b'"success"\n'
        new_percent = database.select('users', 'percent_train', f'email = \'{user_email}\'')[0][0]
        assert new_percent == 99

    def test_add_to_journal(self):
        """Добавление в журнал записи о входе пользователя в систему"""
        dict_login = {
            'email': 'pytest_user@gmail.com',
            'password': base64.b64encode(bytes(str('123456'), "utf-8")).decode('ascii')
        }
        user_id = database.select('users', 'id', f'email = \'{dict_login["email"]}\'')[0][0]

        row_for_delete = [{'user_id': user_id}]
        database.delete('journal', row_for_delete)

        journal_records = database.select('journal', 'id', f'user_id = \'{user_id}\'')
        assert not len(journal_records)

        response = requests.post(f'{host_api_db}:{port_api_db}/database/1.0.0/add-journal', json={'id_user': user_id})
        assert response.content == b'success'

        journal_records = database.select('journal', 'id', f'user_id = \'{user_id}\'')
        assert len(journal_records)

    def test_add_photo(self):
        """Фотография успешно добавляется в базу данных"""
        with open('./tests/face_test.png', 'rb') as f:
            face_img = base64.b64encode(bytes(str(f.read()), "utf-8")).decode('ascii')
        user_email = 'pytest_user@gmail.com'
        user_id = database.select('users', 'id', f'email = \'{user_email}\'')[0][0]

        response = requests.post(f'{host_api_db}:{port_api_db}/database/1.0.0/add-photo',
                                 json=[user_id, face_img])

        assert response.content == b'"success"\n'
        row_for_delete = [{'user_id': user_id}]
        database.delete('photos', row_for_delete)

    def test_update_user(self):
        """" Профиль пользователя успешно изменяется """
        user_id = database.select('users', 'id', f'email = \'pytest_user@gmail.com\'')[0][0]
        dict_user = {
            'id_user': str(user_id),
            'name': 'pytest_user_1',
            'surname': 'pytest_user_1',
            'username': 'pytest_user_1',
            'email': 'pytest_user_1@gmail.com',
            'password': base64.b64encode(bytes('12345678', "utf-8")).decode('ascii')
        }
        response = requests.post(f'{host_api_db}:{port_api_db}/database/1.0.0/update-user', json=dict_user)

        assert response.content == b'success'
        user_id = database.select('users', 'id', f'email = \'{dict_user["email"]}\'')
        assert len(user_id)

    def test_delete_user(self):
        """Пользователь успешно удаляется из БД"""
        email = 'pytest_user_1@gmail.com'
        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/delete-user/' + email)
        assert response.content == b'success'

        user_id = database.select('users', 'id', f'email = \'{email}\'')
        assert not len(user_id)

        row_for_delete = [{'name': device_name}]
        database.delete('device', row_for_delete)

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def exit():
        os._exit(0)
    request.addfinalizer(exit)
