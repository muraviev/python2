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


def log_server(func):
    ''' запись вызова функций сервера
    '''

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        logger.debug(f'запуск функции {func.__name__} : {args} , {kwargs}')
        res = func(*args, **kwargs)
        logger.debug(f'функция {func.__name__} вернула {res}')
        return res
    return wrapped

def log_client(func):
    ''' запись вызова функций  клиента
    '''

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        logger_client.debug(f'запуск функции {func.__name__} : {args} , {kwargs}')
        res = func(*args, **kwargs)
        logger_client.debug(f'функция {func.__name__} вернула {res}')
        return res
    return wrapped
