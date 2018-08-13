from ipaddress import ip_address
import json
import socket
from time import time
from datetime import datetime
import argparse
import decorators
import select
from log_config import logger_srv


class Server:
    pass


class Storage:
    pass


@decorators.log(logger_srv)
def check_srv_sys_args():
    """ проверка наличия системных аргументов
    """
    port = 7777
    ip = '0.0.0.0'
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', action='store', metavar='<port>',
                        help=f'TCP-порт для работы  (по умолчанию использует порт {port})')
    parser.add_argument('-a', action='store', metavar='<ip>',
                        help=f'IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)(например {ip})')

    if parser.parse_args().p:
        try:
            port_tmp = int(parser.parse_args().p)
            if port_tmp not in range(1, 65536):
                raise Exception
            else:
                port = port_tmp
        except:
            print('-' * 80)
            print(f'Ошибка порта, будет использован порт по умолчанию {port}')
            print('Порт необходимо указывать из диапозона 1-65535')
            print('-' * 80)

    if parser.parse_args().a:
        try:
            ip_address(parser.parse_args().a)
            ip = parser.parse_args().a
        except:
            print('-' * 80)
            print(f'Ошибка IP адреса, будет использован IP по умолчанию {ip}')
            print('-' * 80)

    print(f'Настройки соединения: {ip}:{port}')
    return ip, port


def read_requests(r_clients, all_clients):
    ''' Чтение запросов из списка клиентов
    '''
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024)
            data = decode_message(data)
            try:
                data["time"] = f'{datetime.fromtimestamp(data["time"])}'
            except:
                pass
            print(data)
            responses[sock] = data
        except:
            print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    ''' ответ сервера клиентам, от которых были запросы
    '''

    for sock in w_clients:
        if sock in requests:
            try:

                resp = get_response_on_message(requests[sock])
                if resp["response"] == 200:
                    sock.send(json.dumps(resp).encode("utf-8"))
                if resp["response"] == 200 and requests[sock]['action'] == 'msg':
                    data = {
                        "action": "msg",
                        "user": requests[sock]["user"]["account_name"],
                        "message": requests[sock]["message"]
                    }
                    msg_to_all(data, sock, w_clients)

            except:  # Сокет недоступен, клиент отключился
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)


@decorators.log(logger_srv)
def msg_to_all(data, sock, w_clients):
    for client in w_clients:
        try:
            if client != sock:
                client.send(json.dumps(data).encode("utf-8"))
        except:
            pass


@decorators.log(logger_srv)
def ok_response():
    """ ответ сервера 200 Ok
    """

    data = {
        "response": 200,
        "time": time()
    }
    return data


@decorators.log(logger_srv)
def error_response():
    """  ответ сервера 500 -ошибка сервера
    """
    data = {
        "response": 500,
        "time": time(),
        "message": "ошибка запроса"
    }
    print('Error 500')
    return data


@decorators.log(logger_srv)
def get_response_on_message(data):
    """Выбор как отвечать клиенту
    """
    try:
        if data["action"] in ["presence", "msg", "leave", "quit"]:
            return ok_response()
        else:
            return error_response()
    except:
        return error_response()


@decorators.log(logger_srv)
def decode_message(data):
    return json.loads(data.decode("utf-8"))


@decorators.log(logger_srv)
def main(ip, port):
    """ Основной цикл обработки запросов клиентов
    """

    clients = []
    with socket.socket() as sock:
        sock.bind((ip, port))
        sock.listen(5)
        sock.settimeout(0.2)  # Таймаут для операций с сокетом
        while True:
            try:
                client, addr = sock.accept()  # Проверка подключений
            except OSError as e:
                pass  # timeout вышел
            else:
                print(f"Получен запрос на соединение от {addr[0]}:{addr[1]}")
                clients.append(client)
            finally:
                wait = 0
                r = []
                w = []
                try:
                    r, w, e = select.select(clients, clients, [], wait)
                except:
                    pass  # Ничего не делать, если какой-то клиент отключился

                requests = read_requests(r, clients)  # Сохраним запросы клиентов
                write_responses(requests, w, clients)  # Выполним отправку ответов клиентам
