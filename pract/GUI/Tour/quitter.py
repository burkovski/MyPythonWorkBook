"""
кнопка Quit, которая запрашивает подтверждение на завершение;
для повторного использования достаточно прикрепить экземпляр к другому
графическому интерфейсу и скомпоновать с желаемыми параметрами
"""

from tkinter import *
from tkinter.messagebox import askokcancel


class Quitter(Frame):
    def __init__(self, parent=None):
        super(Quitter, self).__init__(parent)
        self.pack()
        widget = Button(self, text='Quit', command=self.quit)
        widget.pack(side=LEFT, expand=YES, fill=BOTH)

    def quit(self):
        answ = askokcancel('Verify exit', 'Really quit?')
        if answ:
            super(Quitter, self).quit()


if __name__ == "__main__":
    Quitter().mainloop()
