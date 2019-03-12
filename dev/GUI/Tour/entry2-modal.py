"""
создает модальный диалог с формой;
данные должны извлекаться до уничтожения окна с полями ввода
"""

from tkinter import *
from entry2 import makeform, fetch, fields


def show(entries, popup):
    fetch(entries)
    popup.destroy()


def ask():
    popup = Toplevel()
    ents = makeform(popup, fields)
    Button(popup, text="OK", command=lambda: show(ents, popup)).pack()
    popup.grab_set()
    popup.focus_set()
    popup.wait_window()


root = Tk()
Button(root, text='Dialog', command=ask).pack()
root.mainloop()
