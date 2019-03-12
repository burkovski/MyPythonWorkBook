"""
############################################################################
реализует логику работы клиента и сервера для передачи произвольного файла
от сервера клиенту через сокет; использует простой протокол с управляющей
информацией вместо отдельных сокетов для передачи управляющих воздействий
и данных (как в ftp), обработка каждого клиентского запроса выполняется
в отдельном потоке, где организован цикл поблочной передачи содержимого
файла; более высокоуровневую схему организации транспортировки вы найдете
в примерах ftplib;
############################################################################
"""

import os
import sys
import time
import threading
from socket import *

blksz = 1024
default_host = "localhost"
default_port = 50001

help_text = """
Usage...
server=> getfile.py -mode server [-port nnn] [-host -hhh|localhost]
client=> getfile.py [-mode client] -file fff [-port nnn] [-host hhh|localhost]
"""


def now():
    return time.asctime()


def parse_cmd():
    keys = {}                           # поместить в словарь для удобства
    args = sys.argv[1:]                 # пропустить имя программы в начале списка аргументов
    while len(args) >= 2:               # пример: keys[-mode] = server
        key, value, *args = args
        keys[key] = value
    return keys


def client(host, port, file_name):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))
    sock.send("{}\n".format(file_name).encode())        # имя файла с каталогом -> bytes
    drop_dir = os.path.split(file_name)[1]              # имя файла в конце пути
    with open(drop_dir, 'wb') as file:                  # создать локальный файл в cwd
        while True:
            data = sock.recv(blksz)                 # получать единовременно до 1 Кб
            if not data:                            # до закрытия сервером
                break
            file.write(data)                        # сохранить данные в локальный файл
    sock.close()
    print("Client got {} at {}".format(file_name, now()))


def server_thread(client_sock):
    sock_file = client_sock.makefile('r')           # обернуть сокет клиентом файла
    file_name = sock_file.readline().rstrip()       # получить имя файла без конца строки
    try:
        file = open(file_name, 'rb')
        while True:
            bytes = file.read(blksz)            # читать/отправлять по 1 Кб
            if not bytes:                       # до полной передачи файла
                break
            sent = client_sock.send(bytes)
            assert sent == len(bytes)
    except Exception:
        print("Error downloading file on server: {}".format(file_name))
    client_sock.close()


def server(host, port):
    server_sock = socket(AF_INET, SOCK_STREAM)      # слушаем сокет TCP/IP
    server_sock.bind((host, port))
    server_sock.listen(5)
    while True:
        client_sock, client_addr = server_sock.accept()
        print("Server connected by {} at {}".format(client_addr, now()))
        threading.Thread(target=server_thread, args=(client_sock, )).start()


def main(args):
    host = args.get("-host", default_host)          # аргуент из cmd или по умолчанию
    port = int(args.get("-port", default_port))     # str -> int
    if args.get("-mode") == "server":               # None если -mode не передан
        if host == "localhost":                     # иначе потерпит неудачу
            host = ""                               # при удаленной работе
        server(host, port)
    elif args.get("-file"):
        client(host, port, args["-file"])           # в режиме клиента нужен файл
    else:
        print(help_text)


if __name__ == "__main__":
    args = parse_cmd()
    main(args)
