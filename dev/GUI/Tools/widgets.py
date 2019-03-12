"""
функции-обертки, упрощающие создание виджетов и опирающиеся на некоторые
допущения (например, режим растягивания); используйте словарь **extras
именованных аргументов для передачи таких параметров настройки, как ширина,
шрифт/цвет и других, и повторно компонуйте возвращаемые виджеты, если компоновка
по умолчанию вас не устраивает;
"""

from tkinter import *


def frame(root, side=TOP, **extras):
    widget = Frame(root)
    return packer(widget, side, **extras)


def label(root, side, text, **extras):
    widget = Label(root, text=text, relief=RIDGE)
    return packer(widget, side, **extras)


def button(root, side, text, command, **extras):
    widget = Button(root, text=text, command=command)
    return packer(widget, side, **extras)


def entry(root, side, link_var, **extras):
    widget = Entry(root, textvariable=link_var, relief=SUNKEN)
    return packer(widget, side, **extras)


def packer(widget, side, **extras):
    widget.pack(side=side, expand=YES, fill=BOTH)
    if extras:
        widget.config(**extras)
    return widget


if __name__ == "__main__":
    root = Tk()
    frm = frame(root)
    label(frm, LEFT, "SPAM")
    button(frm, BOTTOM, "Press", lambda: print("Pushed"))
    root.mainloop()
