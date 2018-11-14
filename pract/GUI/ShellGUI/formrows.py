"""
создает фрейм-ряд с меткой и полем ввода и дополнительной кнопкой, вызывающей
диалог выбора файла; эта реализация была выделена в отдельный модуль, потому что
она может с успехом использоваться и в других программах; вызывающая программа
(или обработчики событий, как в данном случае) должна сохранять ссылку на
связанную переменную на все время использования ряда;
"""

from tkinter import *
from tkinter.filedialog import askopenfilename      # диалог выбора файла


def make_formrow(parent, label, width=15, browse=True, extend=False):
    var = StringVar()
    row = Frame(parent)
    lab = Label(row, text=label+'?', relief=RIDGE, width=width)
    ent = Entry(row, relief=SUNKEN, textvariable=var)
    row.pack(fill=X)                                            # используются фреймы-ряды
    lab.pack(side=LEFT)                                         # с метками фиксированной длины
    ent.pack(side=LEFT, expand=YES, fill=X)                     # можно использовать grid(row, col)
    if browse:
        button = Button(row, text='browse...')
        button.pack(side=RIGHT)
        if not extend:
            action = lambda: var.set(askopenfilename() or var.get())
        else:
            action = lambda: var.set("{} {}".format(var.get(), askopenfilename()))
        button.config(command=action)
    return var
