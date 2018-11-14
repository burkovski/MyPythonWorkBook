"""
На стороне сервера: открывает сокет с указанным номером порта, ожидает
появления сообщения от клиента и отправляет это же сообщение обратно;
продолжает возвращать сообщения клиенту, пока не будет получен признак eof
при закрытии сокета на стороне клиента; для обслуживания клиентов порождает
дочерние потоки выполнения; потоки используют глобальную память совместно
с главным потоком; этот прием является более переносимым, чем ветвление:
потоки выполнения действуют в стандартных версиях Python для Windows,
тогда как прием ветвления – нет;
"""

import time
import threading
from socket import *

my_host = ''
my_port = 50007


sock_obj = socket(AF_INET, SOCK_STREAM)         # создать объект сокета TCP
sock_obj.bind((my_host, my_port))               # связать с номером порта сервера
sock_obj.listen(5)                              # не больше 5 ожидающих запросов в очереди


def now():
    return time.asctime()


def handle_client(connection):              # в дочернем потоке: ответить
    time.sleep(5)                           # имитировать блокирущие действия
    while True:                             # цикл четния-записи в сокет клиента
        data = connection.recv(1024)
        if not data:
            break
        reply = "Echo=>{} at {}".format(data, now())
        connection.send(reply.encode())
    connection.close()


def dispatcher():               # пока процесс работает,
    while True:                 # ждать запроса очередного клиента,
        connection, addres = sock_obj.accept()          # передать потоку для обслуживания
        print("Server connected by: {} at {}".format(addres, now()))
        threading.Thread(target=handle_client, args=(connection, )).start()


dispatcher()
