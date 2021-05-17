import os
"""_____________________________________________________________________
    Configuration file for the "Database" module
    Last modification: 31.03.2021
    Author of the modification: Golyshev Ilya
    Email: ilia.golyshev@t-systems.com
   _____________________________________________________________________"""
__version__ = '1.0.0'

"""_____________________________________________________________________
    Parameters required for configuring paths in the module
        1. Full path to the directory from which the entire module is
           launched
   _____________________________________________________________________"""
"""1"""
work_path = "/home/acs_system"

"""_____________________________________________________________________
    Parameters for connecting to the database
      1. the name of the database
      2. base ip address encoded in base64
      3. the user through which base64-encoded access is performed
      4. the password is encoded in base64
      5. date format
   _____________________________________________________________________"""
"""1"""
db_name = "fra"
"""2"""
host_db = ""
"""3"""
user_db = "cG9zdGdyZXM="
"""4"""
password_db = ""
"""5"""
date_format = "%d.%m.%Y %H:%M:%S"

"""_____________________________________________________________________
    Parameters for configuration logger
      1. format output logger
      2. format output exception logger
      3. name of the folder where the logs are located
      4. name of the log file
      5. Period for creating a new log file
      6. The number of backup files with the logs
   _____________________________________________________________________"""
"""1"""
format_logger = '%(asctime)s - %(filename)-30s - %(levelname)-8s - %(message)s'
"""2"""
str_log_exception = 'EXCEPTION IN ({}, LINE {} "{}"): {}'
"""3"""
dir_log = 'logs'
"""4"""
name_log_file = 'removal_equipment'
"""5"""
period_create_new_log_file = 'midnight'
"""6"""
log_backup_count = 14


"""_____________________________________________________________________
    Parameters for configuring flask API
      1. server host
      2. server ip
      2. server port
   _____________________________________________________________________"""
"""1"""
host = "0.0.0.0"
"""2"""
ip_address = ""
"""3"""
port = "5050"

