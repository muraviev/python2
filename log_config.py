import logging
import pathlib
from logging.handlers import TimedRotatingFileHandler

logger_srv = logging.getLogger('server')
logger_client = logging.getLogger('client')

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s ")

pathlib.Path('logs').mkdir(parents=True, exist_ok=True)

fh = TimedRotatingFileHandler(filename=f"logs/server", when="midnight", interval=1,
                              backupCount=5, encoding='utf-8')
fh_cl = TimedRotatingFileHandler(filename=f"logs/client", when="midnight", interval=1,
                                 backupCount=5, encoding='utf-8')

fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

fh_cl.setLevel(logging.DEBUG)
fh_cl.setFormatter(formatter)

logger_srv.addHandler(fh)
logger_srv.setLevel(logging.DEBUG)

logger_client.addHandler(fh_cl)
logger_client.setLevel(logging.DEBUG)

if __name__ == '__main__':
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger_srv.addHandler(console)
    logger_srv.info('Тестовый запуск логгирования')
    logger_client.addHandler(console)
    logger_client.info('Тестовый запуск логгирования')
