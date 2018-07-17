import sys
from ipaddress import ip_address
import json
import socket


def check_client_sys_args():
    port = 7777
    ip = '127.0.0.1'
    HELP_TEXT = '\r\n'.join((
        '-' * 80,
        '-h - вывод данной справки',
        f'-p <port> - TCP-порт на сервере (по умолчанию использует порт {port})',
        f'-a <addr> - IP-адрес сервера (например {ip})',
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


def client_connect(ip, port):
    sock = socket.socket()
    sock.connect((ip, port))
    result_tmp = ""
    while True:
        data = sock.recv(1024)
        if len(data) == 0:
            break
        result_tmp = data.decode("utf-8")
        result = json.loads(result_tmp)
    sock.close()

    return result
