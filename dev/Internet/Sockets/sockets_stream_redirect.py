"""
############################################################################
Инструменты для подключения стандартных потоков ввода-вывода программ без ГИ
к сокетам, которые программы с графическими интерфейсами (и другие)
могут использовать для взаимодействий с программами без ГИ.
############################################################################
"""

import sys
from socket import *


port = 50008
host = 'localhost'


def init_listener_socket(port=port):
    """
    инициализирует подключеный сокет для вызывающих сценариев,
    которые играют роль сервера
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('', port))           # слушать порт с этим номером
    sock.listen(5)                  # длина очереди ожидающих запросов
    conn, addr = sock.accept()      # ждать подключений клиентов
    return conn


def redirect_out(port=port):
    """
    подключает стандартный поток вывода вызывающей программы к сокету
    для графического интерфейса, уже ожидающего запуск вызывающей программы,
    иначе попытка соединения потерпит неудачу перед вызовом метода accept
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))          # вызывающий сценарий дейсвтует, как клиент
    file = sock.makefile('w')           # интерфейс файла: текстовый режим, буфериз.
    sys.stdout = file                   # обеспечить вызвов sock.send при выводе
    return sock             # на случай, если вызывающему сценарию нужно работать с сокетом напрямую


def redirect_in(port=port, host=host):
    """
    подключает стандартный поток ввода вызывающей программы к сокету
    для получения данных из графического интерфейса
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    file = sock.makefile('r')       # обертка с интерфесом файла
    sys.stdin = file                # обеспечить вызвов sock.recv при вводе
    return sock


def redirect_both_as_client(port=port, host=host):
    """
    подключает стандартные потоки вывода и ввода вызывающей
    программы к одному и тому же сокету;
    в этом режиме вызывающая программа играет роль клиента:
    отпраляет сообшение и получает ответ
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))              # откроем в режиме r+w
    ofile = sock.makefile('w')              # интрефейс файла: текстовый режим, буферизация
    ifile = sock.makefile('r')              # два объекта файла, обертывающих сокет
    sys.stdout = ofile                      # обеспечить вызов sock.send
    sys.stdin = ifile                       # обеспечить вызов sock.recv
    return sock


def redirect_both_as_server(port=port, host=host):
    """
    подключает стандартные потоки ввода и вывода вызывающей
    программы к одному и тому же сокету;
    в этом режиме вызывающая программа играет роль сервера:
    получает сообшение и отпраляет ответ
    """
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((host, port))                 # вызываюший сценарий - сервер
    sock.listen(5)
    conn, addr = sock.accept()
    ofile = conn.makefile('w')              # обертка с интерфейсом файла
    ifile = conn.makefile('r')              # два объекта файла, обертывающих один сокет
    sys.stdout = ofile                      # обеспечить вызов sock.send
    sys.stdin = ifile                       # обеспечить вызов sock.recv
    return conn
