"""
############################################################################
использует FTP для выгрузки всех файлов из локального каталога на удаленный
сайт/каталог; например, сценарий можно использовать для копирования
файлов веб/FTP сайта с вашего ПК на сервер провайдера; выполняет выгрузку
плоского каталога: вложенные каталоги можно копировать с помощью
сценария uploadall.py. дополнительные примечания смотрите в комментариях
в downloadflat.py: этот сценарий является его зеркальным отражением.
############################################################################
"""

import os
import sys
import ftplib

from getpass import getpass
from mimetypes import guess_type


non_passive = False                         # пассивный режим FTP по умолчанию
remote_site = "learning-python.com"         # выгрузить на этот сайт
remote_dir = "books"                        # с компьтера, где выполняется сценарий
remote_user = "username"
remote_pass = getpass("Password for {} on {}".format(remote_user, remote_site))
sign_in = (remote_user, remote_pass) if remote_user and remote_pass else ()
local_dir = sys.argv[1] if len(sys.argv > 1) else '.'
clean_all = input("Clean local directory all?")[:1] in {'y', 'Y'}

print("Connecting...")
conn = ftplib.FTP(remote_site)              # соединиться с FTP-сайтом
conn.login(*sign_in)                        # логин с именем/паролем
conn.cwd(remote_dir)                        # перейти в каталог копирования
if non_passive:
    conn.set_pasv(False)                    # перейти в активный режим FTP

if clean_all:                                           # сначала удалить все локальные файлы
    for remote_name in conn.nlst():                     # чтобы избавиться от устаревших копий os.listdir
        try:
            print("Deleting remote {}".format(remote_name))
            conn.delete(remote_name)
        except Exception:
            print("Cannot delete remote file: {}".format(remote_name))

count = 0                                       # выгрузить все локальные файлы
local_files = os.listdir(local_dir)             # listdir() отбрасывает путь к каталогу

for local_name in local_files:
    mimetype, encoding = guess_type(local_name)
    mimetype = mimetype or "?/?"
    maintype =  mimetype.split('/')[0]
    local_path = os.path.join(local_dir, local_name)
    print("Uploading {} to {} as {} {}".format(local_path, local_name,
                                               maintype, encoding or ''))
    if maintype == "text" and not encoding:
        local_file = open(local_path, 'rb')
        conn.storlines("STOR {}".format(local_name), local_file)
    else:
        local_file = open(local_path, 'rb')
        conn.storbinary("STOR {}".format(local_name), local_file)
    local_file.close()
    count += 1

conn.quit()
print("Done: {} files uploaded.".format(count))
