from tkinter import *
import radactions
from importlib import reload


class Hello(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        buttons = (("message1", self.message1, LEFT),
                   ("message2", self.message2, RIGHT))
        for (text, action, side) in buttons:
            Button(self, text=text, command=action).pack(side=side)

    def message1(self):
        reload(radactions)          # перезагрузить модуль radactions перед вызовом
        radactions.message1()       # теперь щелчок на кнопке вызовет новую версию

    def message2(self):
        reload(radactions)          # изменения в radactions.py возымеют эффект благодаря перезагрузке
        radactions.message2(self)   # вызовет свежую версию; передать self

    def method1(self):
        print("Expose method...")   # вызывается из функции в модуле radactions


Hello().mainloop()
