"""
непосредственное использование виджетов Entry и размещение их по рядам с метками
фиксированной ширины: такой способ компоновки, а также использование менеджера
grid обеспечивают наилучшее представление для форм
"""

from tkinter import *
from quitter import Quitter

fields = ('Name', 'Job', 'Pay')


def fetch(entries):
    for entry in entries:
        print('Input => "{}"'.format(entry.get()))    # извлечь текст


def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)                           # создать новый ряд
        lab = Label(row, width=max(map(len, fields)) + 1, text=field)       # добавить метку, поле ввода
        ent = Entry(row)
        row.pack(side=TOP, fill=X)                  # прикрепить к верхнему краю
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)    # растянуть по горизонтали
        entries.append(ent)
    return entries


if __name__ == '__main__':
    root = Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', lambda event: fetch(ents))
    Button(root, text='Fetch', command=lambda: fetch(ents)).pack(side=LEFT)
    Quitter(root).pack(side=RIGHT)
    root.mainloop()
