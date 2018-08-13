"""
добавляет метку в верхней части окна и возможность растягивания форм
"""

from tkinter import *

colors = ["red", "white", "blue"]


def grid_box(parent=None):
    Label(parent, text="Grid").grid(columnspan=2)
    for row, color in enumerate(colors, start=1):
        label = Label(parent, text=color.capitalize(), relief=RIDGE, width=25)
        entry = Entry(parent, bg=color, relief=SUNKEN, width=50)
        for column, kind in enumerate((label, entry)):
            kind.grid(row=row, column=column, sticky=NSEW)
        parent.rowconfigure(row, weight=1)
    for column in range(2):
        parent.columnconfigure(column, weight=1)


def pack_box(parent=None):
    Label(parent, text="Pack").pack()
    for color in colors:
        row = Frame(parent)
        label = Label(row, text=color.capitalize(), relief=RIDGE, width=25)
        entry = Entry(row, bg=color, relief=SUNKEN, width=50)
        row.pack(side=TOP, expand=YES, fill=BOTH)
        label.pack(side=LEFT, expand=YES, fill=BOTH)
        entry.pack(side=RIGHT, expand=YES, fill=BOTH)


if __name__ == "__main__":
    root = Tk()
    Button(root, text="Quit all", command=root.quit).pack(side=BOTTOM)
    for kind in (grid_box, pack_box):
        kind(Toplevel(root))
    root.mainloop()
