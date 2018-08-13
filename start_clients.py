from subprocess import Popen, CREATE_NEW_CONSOLE

p_list = []

while True:
    user = input("Запустить 10 клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")

    if user == 'q':
        break
    elif user == 's':
        for _ in range(10):
            p_list.append(Popen('python client.py -r',
                                creationflags=CREATE_NEW_CONSOLE))
        print(' Запущено 10 клиентов')
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
