"""
Сервер: обслуживает параллельно несколько клиентов с помощью select.
Использует модуль select для мультиплексирования в группе сокетов:
главных сокетов, принимающих от клиентов новые запросы на соединение,
и входных сокетов, связанных с клиентами, запрос на соединение от которых
был удовлетворен; вызов select может принимать необязательный 4-й аргумент –
0 означает "опрашивать", число n.m означает "ждать n.m секунд", отсутствие
аргумента означает "ждать готовности к обработке любого сокета".
"""

import sys
import time
from select import select
from socket import socket, AF_INET, SOCK_STREAM

my_host = ''
my_port = 50007         # использовать незарезервированый номер порта
num_port_socks = 2           # количество портов для подклчения клиентов
main_socks, read_socks, write_socks = [], [], []    # списки сокетов


def now():
    return time.ctime(time.time())


# создать главные сокеты для приема новых запросов на соединение от клиентов
for i in range(num_port_socks):
    port_sock = socket(AF_INET, SOCK_STREAM)            # создать сокет TCP/IP
    port_sock.bind((my_host, my_port))                  # связать с номером порта сервера
    port_sock.listen(5)                                 # не более 5 ожидающих запросов
    main_socks.append(port_sock)                # добавить в главный список для идентификации
    read_socks.append(port_sock)                # добавить в список источников select
    my_port += 1                                # привязка выполняется к смежным портам


# цикл событий: слушать и мультиплексировать, пока процесс не завершится
print("select-server event loop starting")
while True:
    # print('\n', read_socks)
    read_ables, write_ables, exceptions = select(read_socks, write_socks, [])
    for sock_obj in read_ables:
        if sock_obj in main_socks:              # для готовых входных сокетов
            # сокет порта: принять соединение от нового клиента
            new_sock, address = sock_obj.accept()                   # accept не должен блокировать
            print("Connect: {} {}".format(new_sock, id(new_sock)))   # new_sock - новый сокет
            read_socks.append(new_sock)         # добавить в список обработки select, ждать
        else:
            # сокет клиента: читать следуюзщую строку
            data = sock_obj.recv(1024)          # recv не должен блокировать
            if not data:        # если закрыто клиентом: закрыть и удалить
                sock_obj.close()
                read_socks.remove(sock_obj)
            else:
                # может блокировать: в действительности для операции записи
                # тоже следовало бы использовать вызов select или поток выполнения
                print("\tgot {} on {}".format(data, id(sock_obj)))
                reply = "Echo=>{} at {}".format(data, now())
                sock_obj.send(reply.encode())



