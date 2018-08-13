from my_lib_srv import check_srv_sys_args,serv_open_sock

def test_check_srv_sys_args():
    ip, port = check_srv_sys_args()
    assert ip == '0.0.0.0'
    assert port == 7777

def test_serv_open_sock():
    pass
