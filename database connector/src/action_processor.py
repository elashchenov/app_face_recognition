import config.config as conf
from src.database import DatabaseConnector
from src.logger import get_logger
import psycopg2
import ast
from datetime import datetime

class ActionProcessor:

    def __init__(self):
        self.database = DatabaseConnector(conf.db_name, get_logger())

    def check_user(self, email):
        try:
            _ = self.database.select('users', 'id', f'email = \'{email}\'')[0][0]
            return "exists"
        except:
            self.database.connection.rollback()
            return "doesn't exist"
    
    def login(self, user_data):
        try:
            list_data = self.database.select('users', 'id, name, surname, username, email, password, percent_train', f'email = \'{user_data["email"]}\' and password = \'{user_data["password"]}\'')[0][0]
            print(list_data)
            list_data = tuple(list_data[1:-1].split(","))
            return ("success", list_data)
        except Exception as e:
            print(e)
            self.database.connection.rollback()
            return ("error", [])

    def update_user(self, user_data):
        try:
            self.database.update('users', user_data, f'id = {user_data["id"]}')
            return "success"
        except Exception as e:
            print(e)
            self.database.connection.rollback()
            return "error"
    
    def add_photo(self, photo_data):
        photo_data['image'] = psycopg2.Binary(ast.literal_eval(photo_data['image']))
        try:
            
            self.database.insert('photos', [photo_data])
            return "success"
        except Exception as e:
            print(e)
            self.database.connection.rollback()
            return "error"

    def delete_user(self, email):
        try:
            self.database.delete('users', [
                    {
                        'email': email
                    }
                ])
            return "success"
        except:
            self.database.connection.rollback()
            return "error"

    def add_user(self, user_data):

        if self.check_user(user_data["email"]) == "doesn't exist":
            try:
                id_device = self.database.select('device', 'id', f'name = \'{user_data["device_id"]}\'')[0][0]
                user_data['device_id'] = id_device

                self.database.insert('users', [user_data])
                return "success"
            except Exception as e:
                print(e)
                self.database.connection.rollback()
                return "error"
        else:
            return "exists"


    def add_device(self, name):
        try:
            self.database.insert('device', [
                    {
                        'name': name
                    }
                ])
            return "success"
        except Exception as e:
            print(e)
            self.database.connection.rollback()
            return "error"

    def add_item_to_journal(self, user_id):
        try:
            self.database.insert('journal', [
                    {
                        'user_id': user_id,
                        'date_login': datetime.today()
                    }
                ])
            print('Nice')
            return "success"
        except Exception as e:
            print(e)

            self.database.connection.rollback()
            return "error"

    def get_status_train(self, user_data):
        try:
            percent_train = self.database.select('users','percent_train', f'id = \'{user_data["id_user"]}\'')[0][0]
            return percent_train
        except Exception as e:
            print(e)
            self.database.connection.rollback()
            return "error"

    def set_percent(self, percent, id_user):
        try:
            self.database.update('users', {"percent_train" : int(float(percent))}, f'id = {id_user}')
            return "success"
        except Exception as e:
            print(e)
            self.database.connection.rollback()
            return "error"