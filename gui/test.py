import base64
import cv2
import json
import subprocess

import faulthandler
faulthandler.enable()

from mock import patch
import mock

from PyQt6 import QtWidgets
import os,sys,inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import main

app = QtWidgets.QApplication(sys.argv)
user_profile = ['14','lasdjkf','asdlfkj','eugene', 'eugene.lashchenov@gmail.com','135531', '100']

class TestWindows():

    def test_open_registration(self):
        """Окно Registration успешно открывается из окна Login"""
        window = main.LoginApp()
        window.showReg()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.RegistrationApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is True
        app.closeAllWindows()

    @patch('main.LoginApp.request_creds', return_value=['success', user_profile])
    @patch('requests.post')
    @patch('requests.get')
    def test_open_main(self, mock_request_creds, mock_fake_request, mock_fake_get):
        """Окно main успешно открывается из окна Login при правильных учетных данных"""
        window = main.LoginApp()
        window.showMain()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.MainApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is True
        assert mock_request_creds.called
        assert mock_fake_request.called
        assert mock_fake_get.called
        app.closeAllWindows()

    @patch('main.LoginApp.request_creds', return_value=["error", []])
    def test_not_open_main(self, mock_request_creds):
        """Окно main не открывается из окна Login при неправильных учетных данных"""
        window = main.LoginApp()
        window.showMain()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.MainApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is False
        assert mock_request_creds.called
        app.closeAllWindows()


    @patch('requests.post')
    @patch('requests.get')
    @patch('src.function.get_video_stream', return_value='./tests/face_train.mov')
    def test_open_photo(self, mock_fake_video, mock_req_post, mock_req_get):
        """Окно NewPhoto успешно открывается из окна Registration при нажатии на кнопку Добавить фото и
        после завершения переходит в окно Login"""

        window = main.RegistrationApp()
        list_binary_images_train, list_binary_images_test = window.showDialog()
        assert len(list_binary_images_train) == 160 and len(list_binary_images_test) == 40

        win_opened = True
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.LoginApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is True
        assert mock_req_post.called
        assert mock_req_get.called
        assert mock_fake_video.called
        app.closeAllWindows()

    @patch('requests.get', returned_value=0)
    def test_open_edit(self, mock_req_get):
        """Окно Edit успешно открывается из окна Main при нажатии на кнопку Редактировать данные"""
        window = main.MainApp()
        window.showEdit()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.EditApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is True
        assert mock_req_get.called
        app.closeAllWindows()

    @patch('main.LoginApp.request_creds', return_value=['success', user_profile])
    @patch('main.LoginApp.request_model')
    @patch('src.function.get_video_stream', return_value='./tests/face_train.mov')
    def test_open_resource(self, mock_fake_video, mock_req_model, mock_req_creds):
        """Открытие приложения при вызове метода LoginApp.openResource"""
        subprocess.call(['osascript', '-e', f'tell application "Safari" to quit'])

        with open('./tests/model/model_face.h5', 'rb') as model_binary:
            model_binary = model_binary.read()
            model_enc64 = base64.b64encode(bytes(str(model_binary), "utf-8")).decode('ascii')
            mock_req_model.return_value = bytes(json.dumps(model_enc64, ensure_ascii=False) + "\n", "ascii")

        window = main.LoginApp()
        window.openResource()

        assert mock_req_creds.called
        assert mock_req_model.called
        assert mock_fake_video.called

        subprocess.call(['osascript', '-e', f'tell application "Safari" to quit'])
        app.closeAllWindows()

    def test_close_registration(self):
        """Окно Registration успешно закрывается при нажатии на кнопку Закрыть и переходит в окно Login"""
        window = main.RegistrationApp()
        window.showLogin()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.LoginApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is True
        app.closeAllWindows()

    @patch('requests.get', returned_value=0)
    def test_close_main(self, mock_req_get):
        """Окно Main успешно закрывается при нажатии на кнопку Закрыть и переходит в окно Login"""
        window = main.MainApp()
        window.showLogin()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.LoginApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is True
        assert mock_req_get.called
        app.closeAllWindows()

    @patch('requests.get', returned_value=0)
    def test_close_edit(self, mock_req_get):
        """Окно Edit успешно закрывается при нажатии на кнопку Закрыть и переходит в окно Main"""
        window = main.EditApp()
        window.showMain()

        win_opened = False
        for widget in app.topLevelWidgets():
            print(widget)
            if isinstance(widget, main.MainApp) and not widget.isHidden():
                win_opened = True

        assert win_opened is True
        assert mock_req_get.called
        app.closeAllWindows()

