import sys
from ipaddress import ip_address
import json
import socket
from time import time
from datetime import datetime


def check_client_sys_args():
    port = 7777
    ip = '127.0.0.1'
    HELP_TEXT = '\r\n'.join((
        '-' * 80,
        '-h - вывод данной справки',
        f'-p <port> - TCP-порт на сервере (по умолчанию использует порт {port})',
        f'-a <addr> - IP-адрес сервера (например {ip})',
        '-' * 80))

    if len(sys.argv) == 1 or '-h' in sys.argv:
        print(HELP_TEXT)
    else:
        try:
            ip_address(sys.argv[sys.argv.index('-a') + 1])
            ip = sys.argv[sys.argv.index('-a') + 1]
        except:
            print('-' * 80)
            print(f'Ошибка IP адреса, будет использован IP по умолчанию {ip}')
            print('-' * 80)

        try:
            port_tmp = int(sys.argv[sys.argv.index('-p') + 1])
            if port_tmp not in range(1, 65536):
                raise Exception
            else:
                port = port_tmp
        except:
            print('-' * 80)
            print(f'Ошибка порта, будет использован порт по умолчанию {port}')
            print('Порт необходимо указывать из диапозона 1-65535')
            print('-' * 80)
    print(f'Настройки соединения: {ip}:{port}')

    return ip, port


def format_message(message):  # кодируем сообщение
    return json.dumps(message).encode("utf-8")


def get_user(name, password):
    data = {
        "account_name": name,
        "password": password
    }
    return data


def get_presence_message(user):  # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента Online
    data = {

        "action": "presence",
        "time": time(),
        "type": "status",
        "user": user
    }
    return data


def get_quit_message():  # отключение от сервера
    data = {
        "action": "quit",
        "time": time()
    }
    return data


def main(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))  # Коннект к северу
        while True:
            command = int(input("1. Войти в чат \n"
                                "2. Выйти из чата\n"
                                "******************\n"
                                'Ваш выбор:'))

            if command == 1:
                user = input("Имя пользователя: ")
                password = input("Пароль: ")

                sock.send(
                    format_message(get_presence_message(get_user(user, password))))  # отправка сообщения "присутствие"
                data = sock.recv(1024)
                if data:
                    data = json.loads(data.decode("utf-8"))
                    data["time"] = f'{datetime.fromtimestamp(data["time"])}'
                    print(data)

            elif command == 2:
                sock.send(format_message(get_quit_message()))
                sock.close()
                break
            else:
                print("Неверный ввод")
