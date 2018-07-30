import my_lib_client
import socket
import json

ip, port = my_lib_client.check_client_sys_args()

result, sock = my_lib_client.client_connect(ip, port)
my_lib_client.client_quit(sock)

# print(result.get('msg'))
# print(result.get('action'))
# print(result)


# client_connect(ip=ip, port=port)
