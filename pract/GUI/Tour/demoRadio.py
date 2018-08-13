"""
создает группу переключателей, которые вызывают демонстрационные диалоги
"""

from tkinter import *
from quitter import Quitter
from dialogTable import demos


class Demo(Frame):
    def __init__(self, parent=None, **kwargs):
        super(Demo, self).__init__(parent, **kwargs)
        self.pack()
        Label(self, text="Radio demos").pack(side=TOP)
        self.var = StringVar()
        for key in demos:
            Radiobutton(
                self,
                text=key,
                command=self.on_press,
                variable=self.var,
                value=key
            ).pack(anchor=NW)
        Button(self, text="State", command=self.report).pack(fill=X)
        Quitter(self).pack(fill=X)

    def on_press(self):
        picked = self.var.get()
        print("You pressed:", picked)
        print("Result:", demos[picked]())

    def report(self):
        print(self.var.get())


if __name__ == '__main__':
    Demo().mainloop()
