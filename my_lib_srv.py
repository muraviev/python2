from ipaddress import ip_address
import json
import socket
from time import time
from datetime import datetime
import argparse
import decorators
import select


@decorators.log_server
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


# def check_srv_sys_args():
#     port = 7777
#     ip = '0.0.0.0'
#     HELP_TEXT = '\r\n'.join((
#         '-' * 80,
#         '-h - вывод данной справки',
#         f'-p <port> - TCP-порт для работы  (по умолчанию использует порт {port})',
#         f'-a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)(например {ip})',
#         '-' * 80))
#
#     # print('sys.argv = ', sys.argv)
#
#     if len(sys.argv) == 1 or '-h' in sys.argv:
#         print(HELP_TEXT)
#     else:
#         try:
#             ip_address(sys.argv[sys.argv.index('-a') + 1])
#             ip = sys.argv[sys.argv.index('-a') + 1]
#         except:
#             print('-' * 80)
#             print(f'Ошибка IP адреса, будет использован IP по умолчанию {ip}')
#             print('-' * 80)
#
#         try:
#             port_tmp = int(sys.argv[sys.argv.index('-p') + 1])
#             if port_tmp not in range(1, 65536):
#                 raise Exception
#             else:
#                 port = port_tmp
#         except:
#             print('-' * 80)
#             print(f'Ошибка порта, будет использован порт по умолчанию {port}')
#             print('Порт необходимо указывать из диапозона 1-65535')
#             print('-' * 80)
#     print(f'Настройки соединения: {ip}:{port}')
#     return ip, port


def read_requests(r_clients, all_clients):
    ''' Чтение запросов из списка клиентов
    '''
    responses = {}  # Словарь ответов сервера вида {сокет: запрос}

    for sock in r_clients:
        try:
            data = sock.recv(1024)
            data = json.loads(data.decode("utf-8"))
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
                # Подготовить и отправить ответ сервера
                resp = requests[sock]
                # Эхо-ответ сделаем чуть непохожим на оригинал
                print(get_response_on_message(resp))
                sock.send(get_response_on_message(resp))
            except:  # Сокет недоступен, клиент отключился
                print('Клиент {} {} отключился'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                all_clients.remove(sock)

@decorators.log_server
def ok_response():
    """ ответ сервера 200 Ok
    """

    data = {
        "response": 200,
        "time": time()
    }
    return data

@decorators.log_server
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

@decorators.log_server
@decorators.format_message
def get_response_on_message(data):
    """Выбор как отвечать клиенту
    """
    try:
        if data["action"] == "presence":
            return ok_response()
        elif data["action"] == "leave":
            return ok_response()
        elif data["action"] == "quit":
            return ok_response()
        else:
            return error_response()
    except:
        return error_response()


@decorators.log_server
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

                #
                #
                #
                # while True:
                #     try:
                #         data = client.recv(1024)
                #         if not data:
                #             continue
                #         data = json.loads(data.decode("utf-8"))
                #         data["time"] = f'{datetime.fromtimestamp(data["time"])}'
                #         print(data)
                #
                #         if data["action"] == "quit":
                #             client.close()
                #             break
                #         # client.send(format_message(get_response_on_message(data)))
                #         client.send(get_response_on_message(data))
                #     except:
                #         print('ERROR')
                #         break
