"""
Сценарий на языке Python для загрузки медиафайла по FTP и его проигрывания.
Использует модуль ftplib, реализующий поддержку протокола ftp на основе
сокетов. Протокол FTP использует 2 сокета (один для данных и один
для управления – на портах 20 и 21) и определяет форматы текстовых
сообщений, однако модуль ftplib скрывает большую часть деталей этого
протокола. Измените настройки в соответствии со своим сайтом/файлом.
"""

import os
import sys
from getpass import getpass     # инструмент скрытого ввода пароля
from ftplib import FTP          # инструменты FTP на основе сокетов

nonpassive = False              # использовать активный режим FTP?
file_name = "monkeys.jpg"       # загружаемый файл
dir_name = '.'                  # удаленный диалог, откуда загружаются файлы
site_name = "ftp.rmi.net"       # FTP - сайт, к которому выполняется полклюсение
user_info = ("lutz", getpass("Password?"))      # () для анонимного доступа
if len(sys.argv) > 1: file_name = sys.argv[1]   # имя файла в командной строке


print("Connecting...")
connection = FTP(site_name)     # соединится с FTP сайтом
connection.login(*user_info)    # данные доступа
connection.cwd(dir_name)
if nonpassive:
    connection.set_pasv(False)      # исп. активный режим, если этого требует сервер

print("Downloading...")
local_file = open(file_name, 'wb')      # локальная копия файла
connection.retrbinary("RETR {}".format(file_name), local_file.write, 1024)      # обмен порциями по 1Кб
connection.quit()
local_file.close()

if input("Open file?") in {'Y', 'y'}:
    from pract.SystemProg.Media.playfile import playfile
    playfile(file_name)
