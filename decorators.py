import json
import functools
import sys


def format_message(func):
    ''' возвращает резултат функции в кодировке utf-8
    '''

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return json.dumps(func(*args, **kwargs)).encode("utf-8")

    return wrapped


def log(logger):
    ''' логгирование функций.
    '''

    def call(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger.debug(f'запуск функции {func.__name__} : {args} , {kwargs}')
            logger.debug(f'функция {func.__name__} вызвана из {sys._getframe().f_back.f_code.co_name}')
            res = func(*args, **kwargs)
            logger.debug(f'функция {func.__name__} вернула {res}')
            return res

        return wrapped

    return call
