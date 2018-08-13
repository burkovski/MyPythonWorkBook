"""
использует переменные StringVar
компоновка по колонкам: вертикальные координаты виджетов могут не совпадать
(смотрите entry2)
"""

from tkinter import *
from quitter import Quitter

fields = ('Name', 'Job', 'Pay')


def fetch(vars):
    for var in vars:
        print('Input => "{}"'.format(var.get()))      # извлечь из переменных


def makeform(root, fields):
    form = Frame(root)                  # создать внешний фрейм
    l = Frame(form)                     # создать две колонки
    r = Frame(form)
    form.pack(side=TOP, fill=X)
    l.pack(side=LEFT)
    r.pack(side=RIGHT, expand=YES, fill=X)      # растягивать по горизонтали

    variables = []
    for field in fields:
        lab = Label(l, width=max(map(len, fields)) + 1, text=field)
        ent = Entry(r)
        lab.pack(side=TOP)
        ent.pack(side=TOP, fill=X)
        var = StringVar()
        ent.config(textvariable=var)
        var.set('enter here')
        variables.append(var)

    return variables


if __name__ == '__main__':
    root = Tk()
    vars = makeform(root, fields)
    Button(root, text='Fetch', command=lambda: fetch(vars)).pack(side=LEFT)
    Quitter(root).pack(side=RIGHT)
    root.bind('<Return>', lambda event: fetch(vars))
    root.mainloop()
