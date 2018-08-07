# ---- Пример настройки логгирования для приложения, используя logging ----

# * Logging Cookbook: https://docs.python.org/3/howto/logging-cookbook.html

# logging - стандартный модуль для организации логгирования
import logging
import pathlib
from logging.handlers import TimedRotatingFileHandler

# Быстрая настройка логгирования может быть выполнена так:
# logging.basicConfig(filename="gui.log",
#     format="%(levelname)-10s %(asctime)s %(message)s",
#     level = logging.INFO
# )

# Можно выполнить более расширенную настройку логгирования.
# Создаём объект-логгер с именем db_admin_gui:
logger = logging.getLogger('server')
logger_client = logging.getLogger('client')

# Создаём объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s ")

# Возможные настройки для форматирования:
# -----------------------------------------------------------------------------
# | Формат         | Описание
# -----------------------------------------------------------------------------
# | %(name)s       | Имя регистратора.
# | %(levelno)s    | Числовой уровень важности.
# | %(levelname)s  | Символическое имя уровня важности.
# | %(pathname)s   | Путь к исходному файлу, откуда была выполнена запись в журнал.
# | %(filename)s   | Имя исходного файла, откуда была выполнена запись в журнал.
# | %(funcName)s   | Имя функции, выполнившей запись в журнал.
# | %(module)s     | Имя модуля, откуда была выполнена запись в журнал.
# | %(lineno)d     | Номер строки, откуда была выполнена запись в журнал.
# | %(created)f    | Время, когда была выполнена запись в журнал. Значением
# |                | должно быть число, такое как возвращаемое функцией time.time().
# | %(asctime)s    | Время в формате ASCII, когда была выполнена запись в журнал.
# | %(msecs)s      | Миллисекунда, когда была выполнена запись в журнал.
# | %(thread)d     | Числовой идентификатор потока выполнения.
# | %(threadName)s | Имя потока выполнения.
# | %(process)d    | Числовой идентификатор процесса.
# | %(message)s    | Текст журналируемого сообщения (определяется пользователем).
# -----------------------------------------------------------------------------

# Создаём файловый обработчик логгирования (можно задать кодировку):

pathlib.Path('logs').mkdir(parents=True, exist_ok=True)

# fh = logging.FileHandler(f"logs/server_{datetime.datetime.today().date()}.log", encoding='utf-8')
fh = TimedRotatingFileHandler(filename=f"logs/server", when="midnight", interval=1,
                                    backupCount=5 , encoding='utf-8')
fh_cl = TimedRotatingFileHandler(filename=f"logs/client", when="midnight", interval=1,
                                    backupCount=5 , encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)

fh_cl.setLevel(logging.DEBUG)
fh_cl.setFormatter(formatter)
# Добавляем в логгер новый обработчик событий и устанавливаем уровень логгирования
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)

logger_client.addHandler(fh_cl)
logger_client.setLevel(logging.DEBUG)

# Возможные уровни логгирования:
# -----------------------------------------------------------------------------
# | Уровень важности | Использование
# -----------------------------------------------------------------------------
# | CRITICAL         | log.critical(fmt [, *args [, exc_info [, extra]]])
# | ERROR            | log.error(fmt [, *args [, exc_info [, extra]]])
# | WARNING          | log.warning(fmt [, *args [, exc_info [, extra]]])
# | INFO             | log.info(fmt [, *args [, exc_info [, extra]]])
# | DEBUG            | log.debug(fmt [, *args [, exc_info [, extra]]])
# -----------------------------------------------------------------------------


if __name__ == '__main__':
    # Создаём потоковый обработчик логгирования (по умолчанию sys.stderr):
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)
    # В логгирование передаем имя текущей функции и имя вызвавшей функции
    logger.info('Тестовый запуск логгирования')
