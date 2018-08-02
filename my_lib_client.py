import sys
from ipaddress import ip_address
import json
import socket
from time import time
from datetime import datetime
import decorators


@decorators.log_client
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


@decorators.log_client
def get_user(name, password):
    data = {
        "account_name": name,
        "password": password
    }
    return data


@decorators.log_client
@decorators.format_message
def get_presence_message(user):  # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента Online
    data = {

        "action": "presence",
        "time": time(),
        "type": "status",
        "user": user
    }
    return data


@decorators.log_client
@decorators.format_message
def get_message_message(user,
                        message):  # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента Online
    data = {

        "action": "presence",
        "time": time(),
        "type": "status",
        "user": user,
        "message": message
    }
    return data


@decorators.log_client
@decorators.format_message
def get_quit_message():  # отключение от сервера
    data = {
        "action": "quit",
        "time": time()
    }
    return data


@decorators.log_client
@decorators.format_message
def get_leave_message(user):  # отключение от сервера
    data = {
        "action": "leave",
        "time": time(),
        "user": user,
    }
    return data


@decorators.log_client
def main(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))  # Коннект к северу
        while True:
            command = int(input('1. Чат \n'
                                '2. Выйти из чата\n'
                                '******************\n'
                                'Ваш выбор:'))

            if command == 1:
                name = ''
                password = ''
                while True:
                    command = int(input('1. Ввести логин и пароль\n'
                                        '2. Войти в чат\n'
                                        '3. Выйти из чата\n'
                                        '******************\n'
                                        'Ваш выбор:'))
                    if command == 1:
                        name = input("Имя пользователя: ")
                        password = input("Пароль: ")
                    if command == 2:
                        if name == '' or password == '':
                            name = 'anonymous'
                            password = 'anonymous'
                            print('Выполен анонимный вход')

                        print("Для выходна из чата введите сообщение: exit()")
                        sock.send(get_presence_message(get_user(name, password)))  # отправка сообщения "присутствие"
                        data = sock.recv(1024)
                        if data:
                            data = json.loads(data.decode("utf-8"))
                            data["time"] = f'{datetime.fromtimestamp(data["time"])}'
                            print(data)
                        while True:
                            message = input('*')
                            if message == "exit()":
                                sock.send(get_leave_message(name))
                                data = sock.recv(1024)
                                if data:
                                    data = json.loads(data.decode("utf-8"))
                                    if data["response"] == 200:
                                        print(f'Ответ сервера: {data}')
                                break
                            sock.send(get_message_message(get_user(name, password),
                                                          message))  # отправка сообщения "присутствие"
                            data = sock.recv(1024)
                            if data:
                                data = json.loads(data.decode("utf-8"))
                                if data["response"] == 200:
                                    print(f'Ответ сервера: {data}')
                    if command == 3:
                        break
            elif command == 2:
                sock.send(get_quit_message())
                sock.close()
                break
            else:
                print("Неверный ввод")
