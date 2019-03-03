"""
получает файл с сервера HTTP (web) через сокеты с помощью модуля urllib;
urllib поддерживает протоколы HTTP, FTP, HTTPS и обычные файлы в строках
адресов URL; для HTTP в строке URL можно указать имя файла или удаленного
сценария CGI; смотрите также пример использования urllib в разделе FTP
и вызов сценария CGI в последующей главе; Python позволяет получать файлы
из сети самыми разными способами, различающимися сложностью и требованиями
к серверам: через сокеты, FTP, HTTP, urllib и вывод CGI;
предостережение: имена файлов следует обрабатывать функцией
urllib.parse.quote, чтобы экранировать специальные символы,
если это не делается в программном коде, - смотрите следующие главы;
"""

import sys
from urllib.request import urlopen


show_lines = 6
try:
    server_name, file_name = sys.argv[:1]
except ValueError:
    server_name, file_name = "learning-python.com", "/index.html"

remote_addr = "https://{}{}".format(server_name, file_name)

print(remote_addr)
remote_file = urlopen(remote_addr)
remote_data = remote_file.readlines()
remote_file.close()
for line in remote_data[:show_lines]:
    print(line)
