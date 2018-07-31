from ipaddress import ip_address
import json
import socket
from time import time
from datetime import datetime
import argparse


def check_srv_sys_args():
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

def format_message(dict_message):
    return json.dumps(dict_message).encode("utf-8")


def ok_response():  # ответ сервера об успехе
    data = {
        "response": 200,
        "time": time()
    }
    return data


def error_response():  # ответ сервера об ошибке
    data = {
        "response": 500,
        "time": time()
    }
    return data


def quit_response():  # клиент прислал сообщение: отключение от сервера
    return False


def get_response_on_message(data):  # выбоор как отвечать клиенту
    if data["action"] == "presence":
        return ok_response()
    elif data['action'] == 'quit':
        return quit_response()
    else:
        return error_response()


def main(ip, port):
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
                while True:
                    try:
                        data = client.recv(1024)
                        if not data:
                            continue
                        data = json.loads(data.decode("utf-8"))
                        data["time"] = f'{datetime.fromtimestamp(data["time"])}'
                        print(data)

                        if not get_response_on_message(data):
                            client.close()
                            break
                        client.send(format_message(get_response_on_message(data)))
                    except:
                        print('ERROR')
                        break
