"""
Сценарий на языке Python для загрузки медиафайла по FTP и его проигрывания.
Использует getfile.py, вспомогательный модуль, инкапсулирующий
этап загрузки по FTP.
"""

import getfile
from getpass import getpass

file_name = "monkeys.jpg"


# получить файл с помощью вспомогательного модуля
getfile.getfile(file=file_name,
                site="ftp.rmi.net",
                dir='.',
                user=(),
                refetch=True)


if input("Open file?") in {'y', 'Y'}:
    from dev.SystemProg.Media.playfile import playfile
    playfile(file_name)
