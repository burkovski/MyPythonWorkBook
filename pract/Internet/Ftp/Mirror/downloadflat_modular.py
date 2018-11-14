"""
############################################################################
использует протокол FTP для копирования (загрузки) всех файлов из каталога
на удаленном сайте в каталог на локальном компьютере; эта версия действует
точно так же, но была реорганизована с целью завернуть фрагменты
программного кода в функции, чтобы их можно было повторно использовать
в сценарии выгрузки каталога и, возможно, в других программах в будущем –
в противном случае избыточность программного кода может с течением времени
привести к появлению различий в изначально одинаковых фрагментах и усложнит
сопровождение.
############################################################################
"""

import os
import sys
import ftplib

from getpass import getpass
from mimetypes import guess_type, add_type


default_site = "home.rmi.net"
default_rdir = '.'
default_user = "username"


def config_transfer(site=default_site, rdir=default_rdir, user=default_user):
    """
    принимает параметры выгрузки или загрузки
    из-за большого количества параметров использует класс
    """
    class cf: pass
    cf.non_passive = False
    cf.remote_site = site
    cf.remote_dir = rdir
    cf.remote_user = user
    cf.local_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    cf.clean_all = input("Clean target directory first?")[:1] in {'y', 'Y'}
    cf.remote_pass = getpass("Password for {} on {}:".format(cf.remote_user, cf.remote_site))
    return cf

def is_text_kind(remote_name, trace=True):
    """
    использует mimetype для определения принадлежности файла
    к текстовому или двоичному типу
    'f.html' определяется как ('text/html', None): текст
    'f.jpeg' определяется как ('image/jpeg', None): двоичный
    'f.txt.gz' определяется как ('text/plain', 'gzip'): двоичный
    файлы с неизвестными расширениями определяются как (None, None): двоичные
    модуль mimetype способен также строить предположения об именах
    исходя из типа: смотрите пример PyMailGUI
    """
    add_type("text/x-python-win", ".pyw")
    mimetype, encoding = guess_type(remote_name, strict=False)
    mimetype = mimetype or "?/?"
    maintype = mimetype.split('/')[0]
    if trace: print("\tas {} {}".format(maintype, encoding or ''))
    return maintype == "text" and not encoding


def connect_ftp(cf):
    print("Connecting...")
    connection = ftplib.FTP(cf.remote_site)
    connection.login(cf.remote_user, cf.remote_pass)
    connection.cwd(cf.remote_dir)
    if cf.non_passive:
        connection.set_pasv(False)
    return connection


def clean_locals(cf):
    """
    птыается удалить все локальные файлы, чтобы убрать устаревшие копии
    """
    if cf.clean_all:
        for local_name in os.listdir(cf.localdir):
            try:
                print("Deleting local {}".format(local_name))
                os.remove(os.path.join(cf.local_dir, local_name))
            except Exception:
                print("Cannot delete local {}".format(local_name))


def download_all(cf, connection):
    """
    загружает все файлы из удаленного каталога в соответствии с настройками
    в cf; метод nlst() возвращает список файлов, dir() – полный список
    с дополнительными подробностями
    """
    remote_files = connection.nlst()
    for remote_name in remote_files:
        if remote_name in {'.', '..'}:
            continue
        local_path = os.path.join(cf.local_dir, remote_name)
        print("Downloading {}  to {}".format(remote_name, local_path))
        if is_text_kind(remote_name):
            # текстовый режим передачи
            local_file = open(local_path, 'w', encoding=connection.encoding)
            connection.retrlines("RETR " + remote_name,
                                 lambda line: local_file.write(line + '\n'))
        else:
            # двоичный режим передачи
            local_file = open(local_path, 'wb')
            connection.retrbinary("RETR " + remote_name, local_file.write)
        local_file.close()
    connection.quit()
    print("Done {} file downloaded".format(len(remote_files)))


if __name__ == "__main__":
    cf = config_transfer()
    conn = connect_ftp(cf)
    clean_locals(cf)
    download_all(cf, conn)
