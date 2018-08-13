import my_lib_client

ip, port, mode = my_lib_client.check_client_sys_args()
my_lib_client.main(ip, port, mode)
