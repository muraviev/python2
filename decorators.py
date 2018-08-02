import json
import functools

from log_config import *


def format_message(func):
    ''' возвращает резултат функции в кодировке utf-8
    '''

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return json.dumps(func(*args, **kwargs)).encode("utf-8")

    return wrapped


def log(func):
    ''' запись вызова функций 
    '''

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        res = func(*args, **kwargs)
        logger.debug(f'старт функции {func.__name__} c аргументами {args} {kwargs} вернула {res}')
        return res

    return wrapped
