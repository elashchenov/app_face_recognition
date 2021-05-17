import sys  # sys нужен для передачи argv в QApplication
from PyQt6 import QtWidgets
import src.main_window as main_window  # Это наш конвертированный файл дизайна
import src.edit as edit  # Это наш конвертированный файл дизайна
import src.registration as registration  # Это наш конвертированный файл дизайна
import src.login as login  # Это наш конвертированный файл дизайна
import config.config as config
import os
from key_generator.key_generator import generate
import requests
import time
import base64
import re
import json
import src.function as function
import ast
import subprocess

dict_user = config.dict_user_info
token = ""

class EditApp(QtWidgets.QMainWindow, edit.Ui_EditWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.btn_cancel.clicked.connect(self.showMain)
        self.btn_save.clicked.connect(self.updateData)
        self.txt_name.setText(dict_user["name"])
        self.txt_password.setText(dict_user["password"])
        self.txt_login.setText(dict_user["username"])
        self.txt_surname.setText(dict_user["surname"])
        self.txt_mail.setText(dict_user["email"])
        self.btn_add_photo.clicked.connect(self.showDialog)

    def check_len_data(self, data, name):
        if len(data) == 0:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage(f"Поле {name} должно быть заполнено!")
            return False 
        elif len(data) >= 100:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage(f"Поле {name} должно быть меньше 100 символов!")
            return False
        else:
            return True
    def showMain(self):
        self.window_main = MainApp()
        self.window_main.show()
        self.hide()
    
    def updateData(self):
        if self.check_len_data(self.txt_name.toPlainText(), "Имя"):
            dict_user["name"] = self.txt_name.toPlainText()
        else:
            return 0
        if self.check_len_data(self.txt_surname.toPlainText(), "Фамилия"):
            dict_user["surname"] = self.txt_surname.toPlainText()
        else:
            return 0
        if self.check_len_data(self.txt_login.toPlainText(), "Логин"):
            dict_user["username"] = self.txt_login.toPlainText()
        else:
            return 0
        if self.check_len_data(self.txt_mail.toPlainText(), "Почта"):
            dict_user["email"] = self.txt_mail.toPlainText()
        else:
            return 0
        if self.check_len_data(self.txt_password.text(), "Пароль") and len(self.txt_password.text()) > 3:
            dict_user["password"] = self.txt_password.text()
        else:
            return 0
        pattern = re.compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
        if pattern.match(self.txt_mail.toPlainText()):
            dict_user["password"] = base64.b64encode(bytes(str(self.txt_password.text()),"utf-8")).decode('ascii')
            _ = requests.post(config.api_update_user_info, json=dict_user)
            self.showMain()
        else:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage('Неправильный формат почты!')

 
    def showDialog(self):
        list_binary_images_train, list_binary_images_test = function.add_photo(self.pbar)
        list_binary_images = list_binary_images_train + list_binary_images_test
        for data in list_binary_images:
            _ = requests.post(config.api_add_photo, json=[dict_user["id_user"], data])
        _ = requests.get(config.api_train_model, json=[dict_user["id_user"], list_binary_images_train, list_binary_images_test])
        # print(list_binary_images_train, list_binary_images_test)


class MainApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_edit.clicked.connect(self.showEdit)
        self.btn_cancel.clicked.connect(self.showLogin)
        self.btn_update.clicked.connect(self.updateStatus)
        response = requests.get(config.api_get_status_train, json=dict_user)
        if response:
            percent = int(response.content)
            self.pbar.setValue(percent)
        # self.btn_add_photo.clicked.connect(self.showDialog)
        
    def updateStatus(self):
        percent = int(requests.get(config.api_get_status_train, json=dict_user).content)
        self.pbar.setValue(percent)

    def showLogin(self):
        self.window_login = LoginApp()
        self.window_login.show()
        self.hide()

    def showEdit(self):
        self.window_edit = EditApp()
        self.window_edit.show()
        self.hide()
    
    # def showDialog(self):
    #     fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', r"C:")[0]
    #     img_bytes = open(fname, 'rb').read()
    #     _ = requests.post(config.api_add_photo, json=[dict_user["id_user"], base64.b64encode(bytes(str(img_bytes),"utf-8")).decode('ascii')])


class RegistrationApp(QtWidgets.QMainWindow, registration.Ui_RegistrationWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_cancel.clicked.connect(self.showLogin)
        self.btn_save.clicked.connect(self.saveReg)
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.btn_add_photo.clicked.connect(self.showDialog)
        self.btn_add_photo.setDisabled(True)

    def check_len_data(self, data, name):
        if len(data) == 0:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage(f"Поле {name} должно быть заполнено!")
            return False 
        elif len(data) >= 100:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage(f"Поле {name} должно быть меньше 100 символов!")
            return False
        else:
            return True

    def showLogin(self):
        self.window_login = LoginApp()
        self.window_login.show()
        self.hide()

    def saveReg(self):
        dict_user.clear()
        if self.check_len_data(self.txt_name.toPlainText(), "Имя"):
            dict_user["name"] = self.txt_name.toPlainText()
        else:
            return 0

        if self.check_len_data(self.txt_surname.toPlainText(), "Фамилия"):
            dict_user["surname"] = self.txt_surname.toPlainText()
        else:
            return 0
        if self.check_len_data(self.txt_login.toPlainText(), "Логин"):
            dict_user["username"] = self.txt_login.toPlainText()
        else:
            return 0

        if self.check_len_data(self.txt_mail.toPlainText(), "Почта"):
            dict_user["email"] = self.txt_mail.toPlainText()
        else:
            return 0
        if self.check_len_data(self.txt_password.text(), "Пароль"):
            dict_user["password"] = self.txt_password.text()
        else:
            return 0

        flagCorrect = True
        pattern = re.compile('(^|\s)[-a-z0-9_.]+@([-a-z0-9]+\.)+[a-z]{2,6}(\s|$)')
        if not pattern.match(self.txt_mail.toPlainText()):
            flagCorrect = False
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage('Неправильный формат почты!')
        req = requests.get(config.api_check_user+str(dict_user["email"]))
        
        data_req = str(req.content)

        if data_req[2:-1] == "exists":
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage('Такой пользователь уже существует!')
            flagCorrect = False

        if flagCorrect:
            dict_user["password"] = base64.b64encode(bytes(str(self.txt_password.text()),"utf-8")).decode('ascii')
            dict_user["device_id"] = token
            _ = requests.post(config.api_post_user, json=dict_user)
            self.btn_add_photo.setEnabled(True)
            self.btn_save.setDisabled(True)
            dict_login = config.dict_login
            dict_login["email"] = dict_user["email"]
            dict_login["password"] = dict_user["password"]
            req = requests.get(config.api_get_access, json=dict_login)
            data_req = json.loads(req.content)
            if data_req[0] == "success":
                dict_user["id_user"] = data_req[1][0]
        
    def showDialog(self):
        list_binary_images_train, list_binary_images_test = function.add_photo(self.pbar)
        list_binary_images = list_binary_images_train + list_binary_images_test
        for data in list_binary_images:
            _ = requests.post(config.api_add_photo, json=[dict_user["id_user"], data])
        _ = requests.get(config.api_train_model, json=[dict_user["id_user"], list_binary_images_train, list_binary_images_test])
        self.showLogin()
        return list_binary_images_train, list_binary_images_test


class LoginApp(QtWidgets.QMainWindow, login.Ui_login_Window):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.btn_regist.clicked.connect(self.showReg)
        self.btn_open.clicked.connect(self.showMain)
        self.btn_openResource.clicked.connect(self.openResource)
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_login.setText("eugene.lashchenov@gmail.com")
        self.txt_password.setText("135531")
    
    def showReg(self):
        self.window_reg = RegistrationApp()
        self.window_reg.show()
        self.hide()

    def showMain(self):
        dict_login = config.dict_login
        dict_login["email"] = self.txt_login.toPlainText()
        dict_login["password"] = base64.b64encode(bytes(str(self.txt_password.text()),"utf-8")).decode('ascii')
        data_req = self.request_creds(dict_login)
        if data_req[0] == "success":
            dict_user["name"] = data_req[1][1]
            dict_user["surname"] = data_req[1][2]
            dict_user["username"] = data_req[1][3]
            dict_user["email"] = data_req[1][4]
            dict_user["password"] = data_req[1][5]
            dict_user["id_user"] = data_req[1][0]
            _ = requests.post(config.api_add_journal, json=dict_user)
            self.window_main = MainApp()
            self.window_main.show()
            self.hide()
        else:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage('Неправильный логин или пароль!')

    def request_creds(self, dict_login):
        req = requests.get(config.api_get_access, json=dict_login)
        return json.loads(req.content)

    def openResource(self):
        main_dir = "/Users/lashchenov/university/ТРКПО Маслаков/app_access_with_Face_Recognition/gui"
        dict_login = config.dict_login
        dict_login["email"] = self.txt_login.toPlainText()
        dict_login["password"] = base64.b64encode(bytes(str(self.txt_password.text()),"utf-8")).decode('ascii')
        data_req = self.request_creds(dict_login)
        if data_req[0] == "success":
            dict_user["name"] = data_req[1][1]
            dict_user["surname"] = data_req[1][2]
            dict_user["username"] = data_req[1][3]
            dict_user["email"] = data_req[1][4]
            dict_user["password"] = data_req[1][5]
            dict_user["id_user"] = data_req[1][0]
            percent_train = data_req[1][6]
            if percent_train != '100':
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setWindowTitle('Ошибка')
                error_dialog.showMessage('Модель ещё не обучена!')
                return
            try:
                os.makedirs(os.path.join(main_dir, f"src/models/{dict_user['id_user']}"))
            except:
                pass
            with open(os.path.join(main_dir, f"src/models/{dict_user['id_user']}/model_face.h5"), "wb") as model_binary:
                requested_model = self.request_model()
                model_binary.write(ast.literal_eval(base64.b64decode(requested_model).decode()))
            status = function.openResource(dict_user['id_user'])
            if status:
                subprocess.call(['osascript', '-e', 'tell application \"Safari\"', '-e', 'activate', '-e', 'end tell'])
            else:
                error_dialog = QtWidgets.QErrorMessage(self)
                error_dialog.setWindowTitle('Ошибка')
                error_dialog.showMessage('У вас нет доступа к системе!')
        else:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.setWindowTitle('Ошибка')
            error_dialog.showMessage('Неправильный логин или пароль!')

    def request_model(self):
        model = requests.get(config.api_get_model, json=dict_user).content
        return model

def create_device_token():
    main_dir = '/Users/lashchenov/university/ТРКПО Маслаков/app_access_with_Face_Recognition/gui/'
    global token
    full_path_to_token = os.path.join(main_dir, config.path_to_token)
    with open(full_path_to_token, "a+") as f:
        print(os.stat(full_path_to_token).st_size)
        if os.stat(full_path_to_token).st_size == 0:
            key = generate()
            f.write(key.get_key())
            print(f"{config.api_post_device}{key.get_key()}")
            _ = requests.post(f"{config.api_post_device}{key.get_key()}")
            token = key.get_key()
    with open(full_path_to_token, "r") as f:
        for line in f:
            token = line
            break


def main():
    create_device_token()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = LoginApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

    # print('hello world!')