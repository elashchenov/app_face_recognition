import base64
import os
from datetime import datetime

import config.config as conf
import config.log_msg as log_msg
import config.sql as sql
import psycopg2

"""_____________________________________________________________________________
    Class for connect to database
   _____________________________________________________________________________"""


class DatabaseConnector:

    """__________________________________________________________________________
        Constructor with parameters:
            1. database name - string
            2. logger object
       __________________________________________________________________________"""

    def __init__(self, db_name, logger):
        self.db_name = db_name
        self.user = base64.b64decode(conf.user_db).decode()
        self.password = base64.b64decode(conf.password_db).decode()
        self.host_db = base64.b64decode(conf.host_db).decode()
        self.connection = psycopg2.connect(
            dbname=self.db_name, user=self.user, password=self.password, host=self.host_db)
        self.cursor = self.connection.cursor()
        self.logger = logger

    """__________________________________________________________________________
        Function for SQL transaction select:
            1. table name - string
            2. columns names - string
            3. parameters which add to sql query after key-word WHERE - 
               dictionary(column:value)
        Return:
            list, which contains object with data from database
       __________________________________________________________________________"""

    def select(self, table, column, filter=None):
        if filter:
            filter_ = f"{table} WHERE {filter}"
        else:
            filter_ = f"{table}"
        self.cursor.execute(sql.template_select % (column, filter_))
        return self.cursor.fetchall()

    """__________________________________________________________________________
        Function for SQL transaction insert:
            1. data for insert in database - dictionary(column:value)
            2. table name - string
       __________________________________________________________________________"""

    def insert(self, table, list_data):
        if list_data:
            for item in list_data:
                insert_values, insert_columns = self.convert_dictionary_to_str_for_insert(
                    item)
                self.cursor.execute(sql.template_insert %
                                    (table, insert_columns, insert_values))
                self.connection.commit()

    """__________________________________________________________________________
        Function for convert data from dictionary to string line for SQL 
        transaction insert:
            1. data for convertention - dictionary(column:value)
        Return:
            1. a string that contains data for insert
            2. a string that contains the names of the columns in which the data
               will be inserted 
       __________________________________________________________________________"""

    def convert_dictionary_to_str_for_insert(self, dictionary):
        result_insert = ''
        result_columns = ''

        # loop for input dictionary
        for key, value in dictionary.items():
            result_columns += f'{key}, '

            # check type of data
            if isinstance(value, str):
                result_insert += f'\'{value}\', '
            elif isinstance(value, datetime):
                result_insert += f'to_timestamp(\'{value.strftime(conf.date_format)}\', \'dd.mm.yyyy HH24:MI:SS\'), '
            else:
                result_insert += f'{value}, '
        return result_insert[:-2], result_columns[:-2]

    """__________________________________________________________________________
        Function for SQL transaction update:
            1. table name - string
            2. data for update in database - dictionary(column:value)
            3. parameters which add to sql query after key-word WHERE - 
               dictionary(column:value)
       __________________________________________________________________________"""

    def update(self, table, data, filter=None):
        if filter:
            set_for_update = self.convert_dictionary_to_str_for_update(data)
            self.cursor.execute(sql.template_update %
                                (table, set_for_update, filter))
            self.connection.commit()
        else:
            self.logger.error(log_msg.db_update_error % (table, data, filter))

    """__________________________________________________________________________
        Function for convert data from dictionary to string line for SQL 
        transaction update:
            1. data for convertention - dictionary(column:value)
        Return:
            1. a string that contains data for update
       __________________________________________________________________________"""

    def convert_dictionary_to_str_for_update(self, dictionary):
        result_set = ''

        # loop for input data
        for key, value in dictionary.items():

            # check type
            if isinstance(value, str):
                result_set += f'{key} = \'{value}\', '
            elif isinstance(value, datetime):
                result_set += f'{key} = to_date(\'{value.strftime(conf.date_format)}\', \'dd.mm.yyyy\'), '
            else:
                result_set += f'{key} = {value}, '
        return result_set[:-2].replace("'NULL'", "NULL")

    def delete(self, table, list_data=None):
        if list_data:
            for item in list_data:
                param = table
                param += " WHERE "
                param += self.convert_dictionary_to_str_for_delete(item)
                self.cursor.execute(sql.template_delete % (param))
                self.connection.commit()
                param = None
        else:
            self.cursor.execute(sql.template_delete % (table))
            self.connection.commit()
    
    def convert_dictionary_to_str_for_delete(self, dictionary):
        result_filter = ''
        for key, value in dictionary.items():
            if isinstance(value, str):
                result_filter += f'{key} = \'{value}\' or '
            elif isinstance(value, datetime):
                result_filter += f'{key} = to_date(\'{value.strftime(conf.date_format)}\', \'dd.mm.yyyy\') or '
            else:
                result_filter += f'{key} = {value} or '
        return result_filter[:-3]