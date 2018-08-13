"""
строка меню и панель инструментов прикрепляются к окну в первую очередь, fill=X
(прикрепить первым = обрезать последним); добавляет изображения в элементы меню;
"""

from tkinter import *
from tkinter.messagebox import *


class NewMenuDemo(Frame):                           # расширенный фрейм
    def __init__(self, parent=None, **kwargs):      # прикрепляется к корневому окну?
        Frame.__init__(self, parent, **kwargs)      # вызвать метод суперкласса
        self.master.title("Toolbars and Menus")
        self.create_widgets()
        self.pack(expand=YES, fill=BOTH)

    def create_widgets(self):
        self.make_menubar()
        self.make_toolbar()
        label = Label(self, text="Menu and Toolbar demo")
        label.config(relief=SUNKEN, width=40, height=10, bg="white")
        label.pack(expand=YES, fill=BOTH)

    def make_menubar(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)
        self.file_menu()
        self.edit_menu()
        self.image_menu()

    def make_toolbar(self):
        toolbar = Frame(self, cursor="hand2", relief=SUNKEN, bd=2)
        toolbar.pack(side=BOTTOM, fill=X)
        Button(toolbar, text="Quit", command=self.quit).pack(side=RIGHT)
        Button(toolbar, text="Hello", command=self.greeting).pack(side=LEFT)

    def file_menu(self):
        pulldowm = Menu(self.menubar)
        pulldowm.add_command(label="Open...", command=self.not_done)
        pulldowm.add_command(label="Quit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=pulldowm)

    def edit_menu(self):
        pulldown = Menu(self.menubar)
        pulldown.add_command(label="Paste", command=self.not_done)
        pulldown.add_command(label="Spam", command=self.greeting)
        pulldown.add_separator()
        pulldown.add_command(label="Delete", command=self.greeting)
        pulldown.entryconfig(4, state=DISABLED)
        self.menubar.add_cascade(label="Edit", menu=pulldown)

    def image_menu(self):
        photo_files = (
            "ora-lp4e.gif",
            "pythonPowered.gif",
            "python_conf_ora.gif"
        )
        pulldown = Menu(self.menubar)
        self.photo_objects = []
        for file in photo_files:
            img = PhotoImage(file="../../gifs/" + file)
            pulldown.add_command(image=img, command=self.not_done)
            self.photo_objects.append(img)
        self.menubar.add_cascade(label="Image", menu=pulldown)

    def greeting(self):
        showinfo("Greeting", "Greetings")

    def not_done(self):
        showerror("Not implemented", "Not yet available")

    def quit(self):
        if askyesno("Verify quit", "Are you sure want to quit?"):
            Frame.quit(self)


if __name__ == "__main__":
    NewMenuDemo().mainloop()
