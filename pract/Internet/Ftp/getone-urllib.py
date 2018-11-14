"""
Сценарий на языке Python для загрузки файла по строке адреса URL;
вместо ftplib использует более высокоуровневый модуль urllib;
urllib поддерживает протоколы FTP, HTTP, HTTPS на стороне клиента,
локальные файлы, может работать с прокси-серверами, выполнять инструкции
перенаправления, принимать cookies и многое другое; urllib также
позволяет загружать страницы html, изображения, текст и так далее;
смотрите также парсеры Python разметки html/xml веб-страниц,
получаемых с помощью urllib, в главе 19;
"""

import os
import getpass
from urllib.request import urlopen, urlretrieve      # веб-инструменты на основе сокетов


file_name = "monkeys.jpg"               # имя удаленного/локального файла
password = getpass.getpass("Password?")

remote_addr = "ftp://lutz:{}@ftp.rmi.net/{};type=i".format(password, file_name)
print("Downloading {}".format(remote_addr))

# urlretrieve(remote_addr, file_name)    # такой способ тоже рабоает

remote_file = urlopen(remote_addr)       # возвр. объект типа файла для ввода
local_file = open(file_name, 'wb')       # локальный файл для сохр. данных
local_file.write(remote_file.read())
local_file.close()
remote_file.close()
