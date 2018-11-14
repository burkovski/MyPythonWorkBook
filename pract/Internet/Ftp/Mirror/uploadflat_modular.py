"""
############################################################################
использует FTP для выгрузки всех файлов из локального каталога на удаленный
сайт/каталог; эта версия повторно использует функции из сценария загрузки,
чтобы избежать избыточности программного кода;
############################################################################
"""

import os
from downloadflat_modular import config_transfer, connect_ftp, is_text_kind


def clean_remotes(cf, connection):
    """
    пытается сначала удалить все файлы в каталоге на сервере,
    чтобы ликвидировать устаревшие копии
    """
    if cf.clean_all:
        for remote_name in connection.nlst():
            try:
                print("Deleting remote {}".format(remote_name))
                connection.delete(remote_name)
            except Exception:
                print("Cannot delete remote {}".format(remote_name))


def upload_all(cf, connection):
    """
    выгружает все файлы в каталог на сервере в соответствии с настройками cf
    listdir() отбрасывает пути к каталогам, любые ошибки завершают сценарий
    """
    local_files = os.listdir(cf.local_dir)
    for local_name in local_files:
        local_path = os.path.join(cf.local_dir, local_name)
        print("Uploading {} to {}".format(local_path, local_name))
        if is_text_kind(local_name):
            local_file = open(local_path, 'rb')
            connection.storlines("STOR " + local_name, local_file)
        else:
            local_file = open(local_path, 'rb')
            connection.storbytes("STOR " + local_name, local_file)
        local_file.close()
    connection.quit()
    print("Done: {} files uploaded.".format(len(local_files)))


if __name__ == "__main__":
    cf = config_transfer(site="learning-python.com", rdir="books", user="lutz")
    conn = connect_ftp(cf)
    clean_remotes(cf, conn)
    upload_all(cf, conn)


