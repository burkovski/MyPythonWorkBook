"""
запускает функцию client из модуля getfile и реализует графический
интерфейс на основе многократно используемого класса формы;
с помощью os.chdir выполняет переход в требуемый локальный каталог,
если указан (getfile сохраняет файл в cwd);
что сделать: использовать потоки выполнения, вывести индикатор
хода выполнения операции и отобразить вывод getfile;
"""

from pract.Internet.Sockets.form import Form
from tkinter import Tk, mainloop
from tkinter.messagebox import showinfo
import getfile
import os


class GetFileForm(Form):
    def __init__(self, parent=None, one_shot=False):
        if not parent:
            parent = Tk()
        parent.title("GetFileGui")
        self.parent = parent
        labels = ["Server Name", "Port Number", "File Name", "Local Dir?"]
        super(GetFileForm, self).__init__(labels, parent)
        self.one_shot = one_shot

    def on_submit(self):
        # super(GetFileForm, self).on_submit()
        local_dir = self.content["Local Dir?"].get()
        port_number = int(self.content["Port Number"].get())
        server_name = self.content["Server Name"].get()
        file_name = self.content["File Name"].get()
        if local_dir:
            os.chdir(local_dir)
        getfile.client(server_name, port_number, file_name)
        showinfo("GetFileGui", "Download complete!")
        if self.one_shot:
            self.parent.quit()


if __name__ == "__main__":
    root = Tk()
    GetFileForm(parent=root)
    root.mainloop()
