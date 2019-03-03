"""
получает файл с сервера HTTP (web) через сокеты с помощью модуля http.
client; параметр с именем файла может содержать полный путь к каталогу
и быть именем любого сценария CGI с параметрами запроса в конце,
отделяемыми символом ?, для вызова удаленной программы; содержимое
полученного файла или вывод удаленной программы можно сохранить
в локальном файле, имитируя поведение FTP, или анализировать
с помощью модуля str.find или html.parser; смотрите также описание
метода http.client request(method, url, body=None, hdrs={});
"""

import sys
import http.client


show_lines = 6
try:
    server_name, file_name = sys.argv[1:]
except ValueError:
    server_name, file_name = "www.learning-python.com", "/index.html"

print(server_name, file_name)
server = http.client.HTTPSConnection(server_name)           # Соединиться с http сервером
server.putrequest("GET", file_name)                         # Отправить запрос и заголовки
server.putheader("Accept", "text/html")                     # Можно также отправить запрос POST
server.endheaders()                                         # Как и имена файлов сценариев CGI

reply = server.getresponse()            # Прочитать заголовки и данные ответа
if reply.status != 200:                 # Код 200 означает успех
    print("Error sending request: {}, {}.".format(reply.status, reply.reason))
else:
    data = reply.readlines()            # Объект файла для полчаемых данных
    reply.close()                       # Вывести строки с eoln в конце
    for line in data[:show_lines]:      # Чтобы сохранить, записать в файл
        print(line)                     # Строки уже содержать '\n' но являются строками bytes
    with open("index.html", "wb") as f:
        for line in data:
            f.write(line)
