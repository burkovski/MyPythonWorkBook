"""
На стороне клиента: использует сокеты для передачи данных серверу
и выводит ответ сервера на каждую строку сообщения; 'localhost' означает,
что сервер выполняется на одном компьютере с клиентом, что позволяет
тестировать клиента и сервер на одном компьютере; для тестирования
через Интернет запустите сервер на удаленном компьютере и установите
serverHost или argv[1] равными доменному имени компьютера или его IP-адресу;
сокеты Python являются переносимым интерфейсом к сокетам BSD,
с методами объектов для стандартных функций сокетов, доступных
в системной библиотеке C;
"""

import sys
from socket import *                # переносимый интерфейс сокетов плюс константы


server_host = "localhost"           # имя сервера, например: 'starship.python.net'
server_port = 50007                 # незарезервированный порт, используемый сервером
message = [b"Hello network world"]          # текст, посылаемый серверу обязательно
                                            # типа bytes: b'' или str.encode()
if len(sys.argv) > 1:
    server_host = sys.argv[1]
    if len(sys.argv) > 2:
        message = (x.encode() for x in sys.argv[2:])


sock_obj = socket(AF_INET, SOCK_STREAM)         # создать объект сокета TCP/IP
info = sock_obj.connect((server_host, server_port))    # соединение с сервером и портом

for line in message:
    sock_obj.send(line)                     # послать серверу строчку через сокет
    data = sock_obj.recv(1024)              # получить строку от сервера: до 1k
    print('Client received:', data)         # строка bytes выводится в кавычках, было 'x', repr(x)
sock_obj.close()
