"""
Загружает произвольный файл по FTP. Используется анонимный доступ к FTP,
если не указан кортеж user=(имя, пароль). В разделе самопроверки
используются тестовый FTP-сайт и файл.
"""

from ftplib import FTP              # инструменты FTP на основе сокетов
from os.path import exists          # проверка наличия фалйа


def getfile(file, site, dir, user=(), *, verbose=True, refetch=False):
    """
    загружает файл по ftp с сайта/каталога, используя анонимный доступ
    или дейсвтительную учетную запись, двочиный режим передачи
    """
    if exists(file) and not refetch:
        print("{} already fetched!".format(file))
    else:
        if verbose:
            print("Downloading: {}".format(file))
        with open(file, "wb") as local_file:            # локальный файл имеет то же имя
            remote = FTP(site)                          # соединиться с FTP-сайтом
            remote.login(*user)                         # () для анонимного или (имя, пароль)
            remote.cwd(dir)
            remote.retrbinary("RETR {}".format(file), local_file.write, 1024)
            remote.quit()
        if verbose:
            print("Download done!")


if __name__ == "__main__":
    from getpass import getpass
    file = "monkeys.jpg"
    dir = "."
    site = "ftp.rmi.net"
    user = ("lutz", getpass("Password?"))
    getfile(file, site, dir, user)
