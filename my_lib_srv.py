import sys
from ipaddress import ip_address
import json
import socket
import time
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


def serv_open_sock(ip, port):
    sock = socket.socket()
    sock.bind((ip, port))
    sock.listen(5)
    # timestamp = int(time.time())
    data = {
        "msg": "Добро пожаловать на Наш сервер",
        "action": "probe",
        "time": "",

    }

    while True:
        client, addr = sock.accept()
        print(f"Получен запрос на соединение от {addr[0]}:{addr[1]}")
        data["time"] = int(time.time())
        s_data = json.dumps(data)
        client.send(s_data.encode("utf-8"))
        while True:
            try:
                buf_ = client.recv(1024)
                buf = json.loads(buf_.decode("utf-8"))
                if len(buf) > 0:
                    print(buf, datetime.fromtimestamp(buf['time']))
                    if buf['action'] == 'quit':
                        client.close()
                        break
            except:
                print('ERROR')
                break

