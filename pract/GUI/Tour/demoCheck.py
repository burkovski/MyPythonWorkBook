"""
создает группу флажков, которые вызывают демонстрационные диалоги
"""

from tkinter import *
from quitter import Quitter
from dialogTable import demos


class Demo(Frame):
    def __init__(self, parent=None, **kwargs):
        super(Demo, self).__init__(parent, **kwargs)
        self.pack()
        self.tools()
        Label(self, text="Check demos").pack()
        self.vars = []
        for key in demos:
            var = IntVar()
            Checkbutton(
                self,
                text=key,
                variable=var,
                command=demos[key]
            ).pack(side=LEFT)
            self.vars.append(var)

    def report(self):
        for var in self.vars:
            print(var.get(), end=' ')       # текущие значения флажков: 1 или 0
        print()

    def tools(self):
        frm = Frame(self)
        frm.pack(side=RIGHT)
        Button(frm, text="State", command=self.report).pack(fill=X)
        Quitter(frm).pack(fill=X)


if __name__ == '__main__':
    Demo().mainloop()
