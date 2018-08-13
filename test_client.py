from my_lib_client import check_client_sys_args, client_connect


def test_check_client_sys_args():
    ip, port = check_client_sys_args()
    assert ip == '127.0.0.1'
    assert port == 7777


def test_client_cconnect():
    result, sock = client_connect('127.0.0.1', 7777)
    assert result['msg'] == 'Добро пожаловать на Наш сервер'
    assert result['action'] == 'probe'
