import PyQt6
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtTest import QTest
from mock import patch
import requests
import json
import time
import os, sys, inspect
import base64
import subprocess
import pytest

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import main

app = QtWidgets.QApplication(sys.argv)

dict_user = {"name": 'test_gui',
             "surname": 'test_gui',
             "login": 'test_gui',
             "email": 'test_gui@gmail.com',
             "password": base64.b64encode(bytes(str('123456'), "utf-8")).decode('ascii'),
             "device_id": '3b7f128b2-96a9-3d81f5f9-fd2c062153-6d390e'}

host_api_db = "http://localhost"
port_api_db = "5050"

main.create_device_token()


def find_window(window):
    for widget in app.topLevelWidgets():
        print(widget)
        if isinstance(widget, window) and not widget.isHidden():
            return widget
    return None


def sleep_while_training():
    percent_train = 0
    while percent_train != 100:
        time.sleep(5)
        resp = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/get-status-train',
                            json=dict_user).content
        percent_train = int(resp)


def user_login():
    response = requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/login', json=dict_user)
    data_req = json.loads(response.content)
    assert data_req[0] == "success"
    return data_req


@patch('src.function.get_video_stream', return_value='./tests/face_train.mov')
def test_registration(mock_fake_video):
    """Регистрация пользователя с помощью пользовательского интерфейса"""
    login_window = main.LoginApp()
    QTest.mouseClick(login_window.btn_regist, QtCore.Qt.MouseButtons.LeftButton)
    reg_window = find_window(main.RegistrationApp)
    assert reg_window is not None

    reg_window.txt_name.setText(dict_user["name"])
    reg_window.txt_surname.setText(dict_user["surname"])
    reg_window.txt_login.setText(dict_user["login"])
    reg_window.txt_password.setText('123456')
    reg_window.txt_mail.setText(dict_user["email"])

    QTest.mouseClick(reg_window.btn_save, QtCore.Qt.MouseButtons.LeftButton)
    QTest.mouseClick(reg_window.btn_add_photo, QtCore.Qt.MouseButtons.LeftButton)

    dict_user["id_user"] = user_login()[1][0]

    sleep_while_training()


def test_login():
    """Вход в приложение под правильными учетными данными"""
    login_window = main.LoginApp()
    login_window.txt_login.setText('test_gui@gmail.com')
    login_window.txt_password.setText('123456')
    QTest.mouseClick(login_window.btn_open, QtCore.Qt.MouseButtons.LeftButton)

    main_window = find_window(main.MainApp)
    assert main_window is not None


def test_existing_email():
    """Регистрация пользователя с существующей почтой"""
    user_login()

    login_window = main.LoginApp()
    QTest.mouseClick(login_window.btn_regist, QtCore.Qt.MouseButtons.LeftButton)
    reg_window = find_window(main.RegistrationApp)
    assert reg_window is not None

    reg_window.txt_name.setText(dict_user["name"])
    reg_window.txt_surname.setText(dict_user["surname"])
    reg_window.txt_login.setText(dict_user["login"])
    reg_window.txt_password.setText('123456')
    reg_window.txt_mail.setText(dict_user["email"])
    QTest.mouseClick(reg_window.btn_save, QtCore.Qt.MouseButtons.LeftButton)

    error_window = find_window(QtWidgets.QErrorMessage)
    assert error_window is not None


def test_edit_user_profile():
    """Редактирование пользователя с помощью методов GUI"""
    login_window = main.LoginApp()
    login_window.txt_login.setText('test_gui@gmail.com')
    login_window.txt_password.setText('123456')

    QTest.mouseClick(login_window.btn_open, QtCore.Qt.MouseButtons.LeftButton)
    main_window = find_window(main.MainApp)
    assert main_window is not None

    QTest.mouseClick(main_window.btn_edit, QtCore.Qt.MouseButtons.LeftButton)
    edit_window = find_window(main.EditApp)
    assert edit_window is not None

    dict_user["email"] = 'test_gui_1@gmail.com'
    edit_window.txt_mail.setText(dict_user["email"])
    QTest.mouseClick(edit_window.btn_save, QtCore.Qt.MouseButtons.LeftButton)

    user_login()

@patch('src.function.get_video_stream', return_value='./tests/face_test.mov')
def test_open_resource(mock_fake_video):
    """Доступ к приложению под правильными учетными данными"""
    subprocess.call(['osascript', '-e', 'tell application \"Safari\" to quit'])

    login_window = main.LoginApp()
    login_window.txt_login.setText('test_gui_1@gmail.com')
    login_window.txt_password.setText('123456')
    QTest.mouseClick(login_window.btn_openResource, QtCore.Qt.MouseButtons.LeftButton)

    count = int(subprocess.check_output(["osascript",
                                         "-e", "tell application \"System Events\"",
                                         "-e", "count (every process whose name is \"" + "Safari" + "\")",
                                         "-e", "end tell"]).strip())
    assert count > 0
    assert mock_fake_video.called
    subprocess.call(['osascript', '-e', 'tell application \"Safari\" to quit'])

def test_not_open_resource():
    """Отказ в доступе к приложению под неправильными учетными данными"""
    subprocess.call(['osascript', '-e', 'tell application \"Safari\" to quit'])

    login_window = main.LoginApp()
    login_window.txt_login.setText('aksdjfkasjdlfkjasl;djfa')
    login_window.txt_password.setText('klasjdfajsdklfjalsdjfalks')
    QTest.mouseClick(login_window.btn_openResource, QtCore.Qt.MouseButtons.LeftButton)

    error_window = find_window(QtWidgets.QErrorMessage)
    assert error_window is not None

    count = int(subprocess.check_output(["osascript",
                                         "-e", "tell application \"System Events\"",
                                         "-e", "count (every process whose name is \"" + "Safari" + "\")",
                                         "-e", "end tell"]).strip())
    assert count == 0

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def exit():
        email = 'test_gui_1@gmail.com'
        requests.get(f'{host_api_db}:{port_api_db}/database/1.0.0/delete-user/' + email)
    request.addfinalizer(exit)