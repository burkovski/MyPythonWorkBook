"""
класс, “подмешиваемый” во фреймы: реализует общие методы вызова стандартных
диалогов, запуска программ, простых инструментов отображения текста и так далее;
метод quit требует, чтобы этот класс подмешивался к классу Frame (или его
производным)
"""

from tkinter import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.scrolledtext import *

from .launchmodes import PortableLauncher, System


class GuiMixin:
    def infobox(self, title, text, *args):      # используются стандартные диалоги
        return showinfo(title, text)

    def errorbox(self, text):
        showerror("Error!", text)

    def question(self, title, text, *args):
        return askyesno(title, text)

    def not_done(self):
        showerror("Not implemented!", "Option not available")

    def quit(self):
        answ = self.question("verify quit", "Are you sure want to quit?")
        if answ:
            Frame.quit(self)                    # нерекурсивный вызов quit!

    def help(self):
        self.infobox("Help", "If you wanna you can take!")

    def selectOpenFile(self, file="", dir="."):
        return askopenfilename(initialfile=file, initialdir=dir)

    def selectSaveFile(self, file="", dir="."):
        return asksaveasfilename(initialfile=file, initialdir=dir)

    def clone(self, *args):             # необязательные аргументы конструктора
        new_window = Toplevel()         # создать новую версию
        myclass = self.__class__        # объект класса экземпляра (самого низшего)
        myclass(new_window, *args)             # прикрепить экземпляр к новому окну

    def spawn(self, pycmdline, wait=False):
        if not wait:                                    # запустить новый процесс
            PortableLauncher(pycmdline, pycmdline)()    # запустить программу
        else:
            System(pycmdline, pycmdline)()              # ждать ее завершения

    def browser(self, filename):
        new_window = Toplevel()
        text = ScrolledText(new_window, height=30, width=85)
        text.config(font=("courier", 10, "normal"))
        text.pack(expand=YES, fill=BOTH)
        new_window.title("Text viewer")
        text.insert("0.0", open(filename, 'r').read())


if __name__ == "__main__":
    class TestMixin(GuiMixin, Frame):
        def __init__(self, parent=None):
            Frame.__init__(self, parent)
            self.pack()
            buttons = (
                ("quit", self.quit),
                ("help", self.help),
                ("clone", self.clone),
                ("spawn", self.other)
            )
            for (text, command) in buttons:
                Button(self, text=text, command=command).pack(fill=X)

        def other(self):
            self.spawn("guimixin.py")

    TestMixin().mainloop()
