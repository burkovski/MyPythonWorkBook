"""
############################################################################
тестирование режимов socket_stream_redirection.py
############################################################################
"""

import sys
import os
import multiprocessing
from dev.Internet.Sockets.sockets_stream_redirect import *


#################################################################################
# перенаправление вывода в кленте
#################################################################################

def server1():
    my_pid = os.getpid()
    conn = init_listener_socket()           # блокируется до подключения клиента
    file = conn.makefile('r')
    for i in range(3):                          # читаем вывод клиента
        data = file.readline().rstrip()         # блокируется до поступления данных
        print("server {} got [{}]".format(my_pid, data))     # вывод в окно терминала


def client1():
    my_pid = os.getpid()
    redirect_out()
    for i in range(3):
        print("client {}: {}".format(my_pid, i))    # выводит в сокет
        sys.stdout.flush()                          # иначе останется в буфере до заверщенния прцесса


#################################################################################
# перенаправление ввода в клиенте
#################################################################################

def server2():
    my_pid = os.getpid()            # простой сокет без буферизации
    conn = init_listener_socket()   # отправляет в поток ввода клиента
    for i in range(3):
        conn.send("server {}: {}\n".format(my_pid, i).encode())


def client2():
    my_pid = os.getpid()
    redirect_in()
    for i in range(3):
        data = input()              # ввод из сокета
        print("client {} got [{}]".format(my_pid, data))        # вывод в окно терминала


#################################################################################
# перенаправление ввода и вывода в клиенте, клент является
# клиентом для сокета
#################################################################################

def server3():
    my_pid = os.getpid()
    conn = init_listener_socket()       # ждать подключения клиента
    file = conn.makefile('r')           # принимает print() и передает в input()
    for i in range(3):
        data = file.readline().rstrip()
        conn.send("server {} got [{}]\n".format(my_pid, data).encode())


def client3():
    my_pid = os.getpid()
    redirect_both_as_client()
    for i in range(3):
        print("client {}: {}".format(my_pid, i))        # вывод в сокет
        data = input()                                  # ввод из сокета: выталкивает!
        sys.stderr.write("client {} got [{}]\n".format(my_pid, data))       # не был перенаправлен


#################################################################################
# перенаправление ввода и вывода в клиенте, клиент является
# сервером для сокета
#################################################################################

def server4():
    my_pid = os.getpid()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    file = sock.makefile('r')
    for i in range(3):
        sock.send("server {}: {}\n".format(my_pid, i).encode())     # передать в input()
        data = file.readline().rstrip()                             # принять от print()
        print("server {} got [{}]".format(my_pid, data))            # результат в терминал


def client4():
    my_pid = os.getpid()
    redirect_both_as_server()           # играет роль сервера в этом режиме
    for i in range(3):
        data = input()                  # ввод из сокета: выталкивает выходной буфер
        print("client {} got [{}]".format(my_pid, data))    # вывод в сокет
        sys.stdout.flush()              # иначе посл. порция данных останется в буфере до завершения


#################################################################################
# перенаправление ввода и вывода в клиенте, клиент является клиентом для сокета
# сервер первым инициирует обмен
#################################################################################

def server5():
    my_pid = os.getpid()                # соединение принимает сервер
    conn = init_listener_socket()       # ждать подключения клиента
    file = conn.makefile('r')           # принимает от print() передает в input()
    for i in range(3):
        conn.send("server {}: {}\n".format(my_pid, i).encode())
        data = file.readline().rstrip()
        print("server {} got [{}]".format(my_pid, data))


def client5():
    my_pid = os.getpid()
    redirect_both_as_client()           # играет роль клиента в этом режиме
    for i in range(3):
        data = input()                  # ввод из сокета: выталкивает выходной буфер!
        print("client {} got [{}]".format(my_pid, data))    # вывод в сокет
        sys.stdout.flush()              # иначе посл. порция даных останется в буфере до завершения


# номер выполняемого теста определяется аргументом командной строки
if __name__ == "__main__":
    server = eval("server" + sys.argv[1])
    client = eval("client" + sys.argv[1])               # клиент в этом процессе
    multiprocessing.Process(target=server).start()      # сервер - в новом
    client()                                            # переустановить потоки в клиенте
    # import time; time.sleep(5)    # проверка эфекта выталкиваня буферов при выходе



