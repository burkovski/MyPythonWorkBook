"""
############################################################################
использует протокол FTP для загрузки из удаленного каталога или выгрузки
в удаленный каталог всех файлов сайта; для организации пространства имен
и обеспечения более естественной структуры программного кода в этой версии
используются классы и приемы ООП; мы могли бы также организовать сценарий
как суперкласс, выполняющий загрузку, и подкласс, выполняющий выгрузку,
который переопределяет методы очистки каталога и передачи файла, но это
усложнило бы в других клиентах возможность выполнения обеих операций,
загрузки и выгрузки; для сценария uploadall и, возможно, для других также
предусмотрены методы, выполняющие выгрузку/загрузку единственного файла,
которые используются в цикле в оригинальных методах;
############################################################################
"""

import os
import sys
import ftplib

from getpass import getpass
from mimetypes import guess_type, add_type


dflt_site = "home.rmi.net"
dflt_rdir = '.'
dflt_user = "username"


class FtpTools:
    def get_local_dir(self):
        return sys.argv[1] if len(sys.argv) > 1 else '.'

    def get_clean_all(self):
        return input("Clean target first?")[:1].strip() in {'y', 'Y'}

    def get_password(self):
        return getpass("Password for {} on {}".format(self.remote_user, self.remote_site))

    def config_transfer(self, site=dflt_site, rdir=dflt_rdir, user=dflt_user):
        """
        принимает параметры операции выгрузки или загрузки
        из значений по умолчанию в модуле, из аргументов,
        из командной строки, из ввода пользователя
        анонимный доступ к ftp: user='anonymous' pass=emailaddr
        """
        self.non_passive = False
        self.remote_site = site
        self.remote_dir = rdir
        self.remote_user = user
        self.local_dir = self.get_local_dir()
        self.clean_all = self.get_clean_all()
        self.remote_pass = self.get_password()

    def is_text_kind(self, remote_name, trace=True):
        """
        использует mimetype для определения принадлежности файла
        к текстовому или двоичному типу
        'f.html' определяется как ('text/html', None): текст
        'f.jpeg' определяется как ('image/jpeg', None): двоичный
        'f.txt.gz' определяется как ('text/plain', 'gzip'): двоичный
        неизвестные расширения определяются как (None, None): двоичные
        модуль mimetype способен также строить предположения об именах
        исходя из типа: смотрите пример PyMailGUI
        """
        add_type("text/x-python-win", ".pyw")
        mime_type, encoding = guess_type(remote_name, strict=False)
        mime_type = mime_type or "?/?"
        main_type = mime_type.split('/')[0]
        if trace: print("\tas {} {}".format(main_type, encoding or ''))
        return main_type == "text" and encoding is None

    def connect_ftp(self):
        print("Connecting...")
        connection = ftplib.FTP(self.remote_site)
        connection.login(self.remote_user, self.remote_pass)
        connection.cwd(self.remote_dir)
        if self.non_passive:
            connection.set_pasv(False)
        self.connection = connection

    def clean_locals(self):
        """
        пытается удалить все локальные файлы, чтобы убрать устаревшие копии
        """
        if self.clean_all:
            for local_name in os.listdir(self.local_dir):
                try:
                    print("Deleting local {}".format(local_name))
                    os.remove(os.path.join(self.local_dir, local_name))
                except Exception:
                    print("Cannot delete local {}".format(local_name))

    def clean_remotes(self):
        """
        пытается сначала удалить все файлы в каталоге на сервере,
        чтобы ликвидировать устаревшие копии
        """
        if self.clean_all:
            for remote_name in self.connection.nlst():
                try:
                    print("Deleting remote {}".format(remote_name))
                    self.connection.delete(remote_name)
                except Exception:
                    print("Cannot delete remote {}".format(remote_name))

    def download_one(self, remote_name, local_path):
        """
        загружает один файл по FTP в текстовом или двоичном режиме
        имя локального файла не обязательно должно соответствовать имени
        удаленного файла
        """
        if self.is_text_kind(remote_name):
            local_file = open(local_path, 'w',
                              encoding=self.connection.encoding)
            self.connection.retrlines("RETR " + remote_name,
                                      lambda line: local_file.write(line + '\n'))
        else:
            local_file = open(local_path, 'wb')
            self.connection.retrbinary("RETR " + remote_name, local_file.write)
        local_file.close()

    def upload_one(self, local_name, local_path, remote_name):
        """
        загружает один файл по FTP в текстовом или двоичном режиме
        имя локального файла не обязательно должно соответствовать имени
        удаленного файла
        """
        if self.is_text_kind(local_name):
            local_file = open(local_path, 'rb')
            self.connection.storlines("STOR " + remote_name, local_file)
        else:
            local_file = open(local_path, 'rb')
            self.connection.storbinary("STOR " + remote_name, local_file)
        local_file.close()

    def download_dir(self):
        """
        загружает все файлы из удаленного каталога в соответствии
        с настройками; метод nlst() возвращает список файлов, dir() –
        полный список с дополнительными подробностями
        """
        remote_files = self.connection.nlst()
        for remote_name in remote_files:
            if remote_name in {'.', '..'}:
                continue
            local_path = os.path.join(self.local_dir, remote_name)
            print("Downloading {} to {}".format(remote_name, local_path))
            self.download_one(remote_name, local_path)
        print("Done: {} files downloaded.".format(len(remote_files)))

    def upload_dir(self):
        """
        выгружает все файлы в каталог на сервере в соответствии
        с настройками listdir() отбрасывает пути к каталогам,
        любые ошибки завершают сценарий
        """
        local_files = os.listdir(self.local_dir)
        for local_name in local_files:
            local_path = os.path.join(self.local_dir, local_name)
            print("Uploading {} to {}".format(local_path, local_name))
            self.upload_one(local_name, local_path, local_name)
        print("Done: {} uploaded.".format(len(local_files)))

    def run(self, clean_target=lambda: None, transfer_act=lambda: None):
        """
        выполняет весь сеанс FTP
        по умолчанию очистка каталога и передача не выполняются
        не удаляет файлы, если соединение с сервером установить не удалось
        """
        self.connect_ftp()
        clean_target()
        transfer_act()
        self.connection.quit()


if __name__ == "__main__":
    ftp = FtpTools()
    xfermode = "download"
    if len(sys.argv > 1):
        xfermode = sys.argv.pop(0)

    if xfermode == "download":
        ftp.config_transfer()
        ftp.run(clean_target=ftp.clean_locals, transfer_act=ftp.download_dir)
    elif xfermode == "upload":
        ftp.config_transfer(site="learning-python.com", rdir="books")
        ftp.run(clean_target=ftp.clean_remotes, transfer_act=ftp.upload_dir)
    else:
        print("Usage: ftptools.py [download | upload][local_dir]")
