from PyQt6 import QtWidgets
import cv2
import mock
from mock import patch
import os,sys,inspect
import requests
import json
import base64
import faulthandler
import subprocess
import pytest
import time
faulthandler.enable()

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import main

app = QtWidgets.QApplication(sys.argv)
dict_user = {"name": 'test_gui',
             "surname": 'test_gui',
             "login": 'test_gui',
             "email": 'test_gui@gmail.com',
             "password": base64.b64encode(bytes(str('123456'),"utf-8")).decode('ascii'),
             "device_id": '3b7f128b2-96a9-3d81f5f9-fd2c062153-6d390e'}

host_api_db = "http://localhost"
port_api_db = "5050"

class TestFullApp():

    @patch('src.function.get_video_stream', return_value='./tests/face_train.mov')
    def test_create_user(self, mock_fake_video):
        """Проверка функционала регистрации нового пользователя"""
        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/login', json=dict_user)
        assert response.content == b'["error", []]\n'

        main.create_device_token()
        window = main.RegistrationApp()
        window.txt_name.setText(dict_user["name"])
        window.txt_surname.setText(dict_user["surname"])
        window.txt_login.setText(dict_user["login"])
        window.txt_password.setText('123456')
        window.txt_mail.setText(dict_user["email"])
        window.saveReg()

        window.showDialog()

        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/login', json=dict_user)
        data_req = json.loads(response.content)
        assert data_req[0] == "success"

        assert mock_fake_video.called

        dict_user["id_user"] = data_req[1][0]
        percent_train = 0
        while percent_train != 100:
            time.sleep(5)
            resp = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/get-status-train', json=dict_user).content
            percent_train = int(resp)


    def test_user_login(self):
        """Успешный вход при отправке правильных учетных данных"""
        main.create_device_token()
        window = main.LoginApp()
        window.txt_login.setText('test_gui@gmail.com')
        window.txt_password.setText('123456')
        window.showMain()

        win_opened = False
        for widget in app.topLevelWidgets():
            if isinstance(widget, main.MainApp) and not widget.isHidden():
                win_opened = True
        assert win_opened

    def test_create_existing_user(self):
        """Отказ на попытку отправить запрос на регистрацию пользователя с существующими данными"""
        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/login', json=dict_user)
        data_req = json.loads(response.content)
        assert data_req[0] == "success"

        main.create_device_token()
        window = main.RegistrationApp()
        window.txt_name.setText(dict_user["name"])
        window.txt_surname.setText(dict_user["surname"])
        window.txt_login.setText(dict_user["login"])
        window.txt_password.setText('123456')
        window.txt_mail.setText(dict_user["email"])
        window.saveReg()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, QtWidgets.QErrorMessage) and not widget.isHidden():
                win_opened = True
        assert win_opened


    def test_edit_user(self):
        """Запрос на редактирование информации существующего пользователя"""
        main.create_device_token()
        window = main.LoginApp()
        window.txt_login.setText('test_gui@gmail.com')
        window.txt_password.setText('123456')

        window.showMain()
        main_window = window.window_main
        main_window.showEdit()
        dict_user["email"] = 'test_gui_1@gmail.com'
        main_window.window_edit.txt_mail.setText(dict_user["email"])
        main_window.window_edit.updateData()

        response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/login', json=dict_user)
        data_req = json.loads(response.content)
        assert data_req[0] == "success"

    @patch('src.function.get_video_stream', return_value='./tests/face_test.mov')
    def test_open_resource(self, mock_fake_video):
        """Запрос на доступ к ресурсу с правильными учетными данными"""
        subprocess.call(['osascript', '-e', 'tell application \"Safari\" to quit'])

        window = main.LoginApp()
        window.txt_login.setText('test_gui_1@gmail.com')
        window.txt_password.setText('123456')
        window.openResource()

        count = int(subprocess.check_output(["osascript",
                                             "-e", "tell application \"System Events\"",
                                             "-e", "count (every process whose name is \"" + "Safari" + "\")",
                                             "-e", "end tell"]).strip())
        assert count > 0
        assert mock_fake_video.called
        subprocess.call(['osascript', '-e', 'tell application \"Safari\" to quit'])

    def test_not_open_resource(self):
        """Отказ доступа к ресурсу с неправильными учетными данными"""
        subprocess.call(['osascript', '-e', 'tell application \"Safari\" to quit'])

        window = main.LoginApp()
        window.txt_login.setText('aksdjfkasjdlfkjasl;djfa')
        window.txt_password.setText('klasjdfajsdklfjalsdjfalks')
        window.openResource()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, QtWidgets.QErrorMessage) and not widget.isHidden():
                win_opened = True
        assert win_opened
        count = int(subprocess.check_output(["osascript",
                                             "-e", "tell application \"System Events\"",
                                             "-e", "count (every process whose name is \"" + "Safari" + "\")",
                                             "-e", "end tell"]).strip())
        assert count == 0

    @patch('src.function.get_video_stream', return_value='./tests/face_fail.mov')
    def test_stranger_face(self, mock_fake_video):
        """Не пропустить пользователя с незарегестрированным лицом"""
        app.closeAllWindows()
        subprocess.call(['osascript', '-e', 'tell application \"Safari\" to quit'])
        main.create_device_token()

        login_window = main.LoginApp()
        login_window.txt_login.setText('test_gui_1@gmail.com')
        login_window.txt_password.setText('123456')
        login_window.openResource()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, QtWidgets.QErrorMessage) and not widget.isHidden():
                win_opened = True
        assert win_opened
        assert mock_fake_video.called

        count = int(subprocess.check_output(["osascript",
                                             "-e", "tell application \"System Events\"",
                                             "-e", "count (every process whose name is \"" + "Safari" + "\")",
                                             "-e", "end tell"]).strip())
        assert count == 0

    @patch('src.function.get_video_stream', return_value='./tests/face_test.mov')
    def test_block_when_training(self, mock_fake_video):
        """Блокировать доступ к приложению пока модель обучается"""
        main.create_device_token()

        login_window = main.LoginApp()
        login_window.txt_login.setText('test_gui_1@gmail.com')
        login_window.txt_password.setText('123456')
        login_window.showMain()

        main_window = login_window.window_main
        main_window.showEdit()

        edit_window = main_window.window_edit
        edit_window.showDialog()
        edit_window.showMain()
        time.sleep(10)

        main_window = edit_window.window_main
        main_window.showLogin()

        login_window = main_window.window_login
        login_window.txt_login.setText('test_gui_1@gmail.com')
        login_window.txt_password.setText('123456')
        login_window.openResource()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, QtWidgets.QErrorMessage) and not widget.isHidden():
                win_opened = True
        assert win_opened
        assert mock_fake_video.called

        percent_train = 0
        while percent_train != 100:
            time.sleep(5)
            resp = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/get-status-train', json=dict_user).content
            percent_train = int(resp)

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def exit():
        email = 'test_gui_1@gmail.com'
        requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/delete-user/' + email)
    request.addfinalizer(exit)











