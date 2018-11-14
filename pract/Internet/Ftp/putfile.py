"""
Выгружает произвольный файл по FTP в двоичном режиме.
Использует анонимный доступ к ftp, если функции не был передан
кортеж user=(имя, пароль) аргументов.
"""

import ftplib                   # инструменты FTP на основе сокетов


def put_file(file, site, dir, user=(), *, verbose=True):
    """
    выгружает произвольный файл по FTP на сайт/каталог, используя анонимный
    доступ или действительную учетную запись, двоичный режим передачи
    """
    if verbose:
        print("Uploading: {}".format(file))
    with open(file, 'rb') as local:         # локальный файл с тем же именем
        remote = ftplib.FTP(site)           # соеденится с FTP сайтом
        remote.login(*user)                 # анонимная или действительная учетная запись
        remote.cwd(dir)
        remote.storbinary("STOR {}".format(file), local, 1024)
        remote.quit()
    if verbose:
        print("Upload done!")


if __name__ == "__main__":
    site = "ftp.rmi.net"
    dir = "."
    import sys
    put_file(sys.argv[1], site, dir, user=())       # имя файла в ком. строке, анонимная учетная запись
