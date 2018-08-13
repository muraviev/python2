import my_lib_srv

ip, port = my_lib_srv.check_srv_sys_args()
my_lib_srv.main(ip=ip, port=port)
