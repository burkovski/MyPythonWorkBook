"""
############################################################################
использует протокол FTP для копирования (загрузки) всех файлов
из единственного каталога на удаленном сайте в каталог на локальном
компьютере; запускайте этот сценарий периодически для создания зеркала
плоского каталога FTP-сайта, находящегося на сервере вашего провайдера;
для анонимного доступа установите переменную remoteuser в значение
'anonymous'; чтобы пропускать ошибки загрузки файлов, можно было бы
использовать инструкцию try, но в случае таких ошибок FTP-соединение скорее
всего все равно будет закрыто автоматически; можно было бы перед передачей
каждого нового файла переустанавливать соединение, создавая новый экземпляр
класса FTP: сейчас устанавливается всего одно соединение; в случае неудачи
попробуйте записать в переменную nonpassive значение True, чтобы
использовать активный режим FTP, или отключите брандмауэр; кроме того,
работоспособность этого сценария зависит от настроек сервера FTP
и возможных ограничений на загрузку.
############################################################################
"""

import os
import sys
import ftplib

from getpass import getpass
from mimetypes import guess_type


non_passive = False             # по умолчанию - пассиваный режим FTP
remote_site = "home.rmi.net"    # загрузить с этого сайта
remote_dir = '.'                # и из этого каталога
remote_user = ""
remote_pass = getpass("Password for {} on {}".format(remote_user, remote_site))
sign_in = (remote_user, remote_pass) if remote_user and remote_pass else ()
local_dir = sys.argv[1] if len(sys.argv > 1) else '.'
clean_all = input("Clean local directory all?")[:1] in {'y', 'Y'}


print("Connecting...")
conn = ftplib.FTP(remote_site)          # соеденится с FTP сайтом
conn.login(*sign_in)                    # зарегестрироваться с именем/паролем
conn.cwd(remote_dir)                    # перейти в копируемый каталог
if non_passive:
    conn.set_pasv(False)                # перевод в активный режим пренудительно

if clean_all:                                           # сначала удалить все локальные файлы
    for local_file in os.listdir(local_dir):            # чтобы избавиться от устаревших копий os.listdir
        try:
            print("Deleting local {}".format(local_file))
            os.remove(os.path.join(local_dir, local_file))
        except Exception:
            print("Cannot delete local file: {}".format(local_file))

count = 0                       # загрузить все файлы из удаленного каталога
remote_files = conn.nlst()      # nlst() возвращает список файловб dir() - полный список
for remote_file in remote_files:
    if remote_file in {'.', '..'}:          # некоторые серверы включают '.' и '..'
        continue
    mimetype, encoding = guess_type(remote_file)        # например ('text/plain', 'gzip')
    mimetype = mimetype or "?/?"                        # допускается (None, None)
    maintype = mimetype.split("/")[0]                   # .jpg ('image/jpeg', None)
    local_path = os.path.join(local_dir, remote_file)
    print("Downloading {}  to {} as  {} {}".format(remote_file, local_path,
                                                   maintype, encoding or ''))
    if maintype == "text" and not encoding:
        # использовать текстовый режим передачи и кодировку, совместимую с ftplib
        local_file = open(local_path, 'w', encoding=conn.encoding)
        callback = lambda line: local_file.write(line + '\n')
        conn.retrlines("RETR {}".format(remote_file), callback)
    else:
        # передать двочиный файл, импользуя двоичный режим передачи
        local_file = open(local_path, 'wb')
        conn.retrbinary("RETR {}".format(remote_file), local_file.write)
    local_file.close()
    count += 1

conn.quit()
print("Done: {} files downloaded".format(count))
