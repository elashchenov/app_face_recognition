import logging
import logging.config as conf
import os
from logging.handlers import TimedRotatingFileHandler

import config.config as conf

"""_______________________________________________________________
    Function need to create object Logger to logging interactions 
    with API
    Input:
    Output: 
        object Logger
    _______________________________________________________________"""


def get_logger():

    # creating a folder for logs if it is not available
    # full_path_to_logs = os.path.join(conf.work_path, conf.dir_log)
    # if not os.path.exists(full_path_to_logs):
    #     os.mkdir(full_path_to_logs)
    # full_path_to_logs = os.path.join(full_path_to_logs, conf.name_log_file)

    # initialization of logger
    logger = logging.getLogger(str(__file__)[:-3])

    # creating a handler that writes to a file and re-creates it in time
    # handler = TimedRotatingFileHandler(
    #     full_path_to_logs, when=conf.period_create_new_log_file, backupCount=conf.log_backup_count)
    # handler.setLevel(logging.INFO)
    # handler.setFormatter(logging.Formatter(conf.format_logger))
    # logger.addHandler(handler)
    #
    # # creating a handler that is necessary for logging when starting the module via systemctl
    # log = journal.JournalHandler()
    # log.setLevel(logging.INFO)
    # log.setFormatter(logging.Formatter(conf.format_logger))
    # logger.addHandler(log)
    # logger.setLevel(logging.INFO)
    return logger
