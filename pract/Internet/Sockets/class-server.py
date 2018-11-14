"""
На стороне сервера: открывает сокет на указанном порту, ожидает поступления
сообщения от клиента и отправляет его обратно; эта версия использует
стандартный модуль socketserver; модуль socketserver предоставляет классы
TCPServer, ThreadingTCPServer, ForkingTCPServer, их варианты для протокола
UDP и многое другое, передает каждый запрос клиента на соединение методу
handle нового экземпляра указанного объекта обработчика; кроме того,
модуль socketserver поддерживает доменные сокеты Unix, но только
в Unix-подобных системах; смотрите руководство по стандартной
библиотеке Python.
"""

import socketserver     # получить серверы сокетов, объекты-обработчики
import time


my_host = ''                        # компьютер-сервер, '' означает локальный хост
my_port = 50007                     # использовать незарезервированный номер порта


def now():
    return time.asctime()


class MyClientHandler(socketserver.BaseRequestHandler):
    def handle(self):                                       # для каждого клиента
        print(self.client_address, now())                   # показать адрес этого клиента
        time.sleep(5)                                       # имитировать блокирующие действия
        while True:
            data = self.request.recv(1024)                  # self.request - сокет клиента
            if not data:                                    # чтение, запись в сокет клиента
                break
            reply = "Echo=>{} at {}".format(data, now)
            self.request.send(reply.encode())
        self.request.close()


# создать сервер с поддержекой многопоточной модели выполнения,
# слушать/обслуживать клиентов непрерывно
my_addr = (my_host, my_port)
server = socketserver.ThreadingTCPServer(my_addr, MyClientHandler)
server.serve_forever()
