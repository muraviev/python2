import sys
from ipaddress import ip_address
import json
import socket


def check_srv_sys_args():
    port = 7777
    ip = '0.0.0.0'
    HELP_TEXT = '\r\n'.join((
        '-' * 80,
        '-h - вывод данной справки',
        f'-p <port> - TCP-порт для работы  (по умолчанию использует порт {port})',
        f'-a <addr> - IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)(например {ip})',
        '-' * 80))

    # print('sys.argv = ', sys.argv)

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


def serv_open_sock(ip, port):
    sock = socket.socket()
    sock.bind((ip, port))
    sock.listen(1)

    data = {
        "msg": "Добро пожаловать на Наш сервер",
        "action": "do_smth"
    }
    s_data = json.dumps(data)

    while True:
        client, addr = sock.accept()
        print(f"Получен запрос на соединение от {addr[0]}:{addr[1]}")
        client.send(s_data.encode("utf-8"))
        client.close()
