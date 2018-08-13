"""
проверка состояния флажков, простой способ
"""

from tkinter import *

root = Tk()
states = {}


for i in range(10):
    var = BooleanVar()
    Checkbutton(
        root,
        text=str(i),
        variable=var,
        command=(
            lambda: print({key: states[key].get() for key in states})
        )
    ).pack(side=LEFT)
    states[i] = var

root.mainloop()
