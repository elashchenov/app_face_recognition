import linecache
import sys
import config.config as config

"""_______________________________________________________________
    (PrintException)function need to print fromat exception
    Output: 
        string exception
    _______________________________________________________________"""
def PrintException():
    _, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    return(config.str_log_exception%(filename, lineno, line.strip(), exc_obj))