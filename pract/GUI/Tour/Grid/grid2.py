"""
добавляет эквивалентное окно, используя фреймы-ряды и метки фиксированной длины;
использование фреймов-колонок не обеспечивает точного взаимного расположения
виджетов Label и Entry по горизонтали; программный код в обоих случаях имеет
одинаковую длину, хотя применение встроенной функции enumerate позволило бы
сэкономить 2 строки в реализации компоновки по сетке;
"""

from tkinter import *


COLORS = ["red", "green", "orange", "white", "yellow", "blue"]


def grid_box(parent=None):
    """
    компоновка по номерам рядов/колонок в сетке
    """
    for row, color in enumerate(COLORS):
        label = Label(parent, text=color.capitalize(), relief=RIDGE, width=25)
        entry = Entry(parent, bg=color, relief=SUNKEN, width=50)
        label.grid(row=row, column=0)
        entry.grid(row=row, column=1)
        entry.insert(0, "grid")


def pack_box(parent=None):
    """
    фреймы-ряды и метки фиксированной длины
    """
    for color in COLORS:
        row = Frame(parent)
        row.pack(side=TOP)
        Label(row, text=color.capitalize(), relief=RIDGE, width=25).pack(side=LEFT)
        entry = Entry(row, bg=color, relief=SUNKEN, width=50)
        entry.pack(side=RIGHT)
        entry.insert(0, "pack")


if __name__ == "__main__":
    root = Tk()
    grid_box(Toplevel())
    pack_box(Toplevel())
    Button(root, text="Quit", command=root.quit).pack()
    root.mainloop()
