"""
############################################################################
вызывает функцию FTP getfile из многократно используемого класса формы
графического интерфейса; использует os.chdir для перехода в целевой
локальный каталог (getfile в настоящее время предполагает,
что в имени файла отсутствует префикс пути к локальному каталогу);
вызывает getfile.getfile в отдельном потоке выполнения, что позволяет
выполнять несколько запросов одновременно и избежать блокировки
графического интерфейса на время загрузки; отличается от основанного
на сокетах getfilegui, но повторно использует класс Form построителя
графического интерфейса; в данном виде поддерживает как анонимный доступ
к FTP, так и с указанием имени пользователя;
предостережение: содержимое поля ввода пароля здесь не скрывается
за звездочками, ошибки выводятся в консоль, а не в графический интерфейс
(потоки выполнения не могут обращаться к графическому интерфейсу в Windows),
поддержка многопоточной модели выполнения реализована не на все 100%
(существует небольшая задержка между os.chdir и открытием локального
выходного файла в getfile) и можно было бы выводить диалог "сохранить как",
для выбора локального каталога, и диалог с содержимым удаленного каталога,
для выбора загружаемого файла; читателям предлагается самостоятельно
добавить эти улучшения;
############################################################################
"""

from tkinter import Tk, mainloop
from tkinter.messagebox import showinfo
import getfile
import os
import sys
import threading
from pract.Internet.Sockets.form import Form        # использовать инструмент форм


class FtpForm(Form):
    def __init__(self, root):
        root.title(self.title)
        labels = ["Server Name", "Remote Dir", "File Name",
                  "Local Dir", "User Name?", "Password?"]
        super(FtpForm, self).__init__(labels, root)
        self.mutex = threading.Lock()
        self.threads = 0
        self.labels = labels
        self.parent = root

    def transfer(self, file_name, server_name, remote_dir, user_info):
        try:
            self.do_transfer(file_name, server_name, remote_dir, user_info)
            print("{} of {} successful".format(self.mode, file_name))
        except Exception as exc:
            print("{} of {} failed: {}".format(self.mode, file_name, exc))
        self.mutex.acquire()
        self.threads -= 1
        self.mutex.release()

    def on_submit(self):
        super(FtpForm, self).on_submit()
        local_dir = self.content["Local Dir"].get()
        remote_dir = self.content["Remote Dir"].get()
        server_name = self.content["Server Name"].get()
        file_name = self.content["File Name"].get()
        user_name = self.content["User Name?"].get()
        password = self.content["Password?"].get()
        user_info = (user_name, password) if user_name and password else ()
        if local_dir:
            os.chdir(local_dir)
        self.mutex.acquire()
        self.threads += 1
        self.mutex.release()
        ftp_args = (file_name, server_name, remote_dir, user_info)
        threading.Thread(target=self.transfer, args=ftp_args).start()
        showinfo(self.title, "{} of {} started".format(self.mode, file_name))

    def on_cancel(self):
        if self.threads:
            showinfo(self.title, "Cannot exit: {} threads running!".format(self.threads))
        else:
            self.parent.quit()


class FtpGuiForm(FtpForm):
    title = "FtpGetfileGui"
    mode = "Download"
    def do_transfer(self, file_name, server_name, remote_dir, user_info):
        getfile.getfile(file_name, server_name, remote_dir, user_info,
                        verbose=False, refetch=True)


if __name__ == "__main__":
    root = Tk()
    FtpGuiForm(root=root)
    root.mainloop()
