"""
Меню на основе фреймов: пригодно для окон верхнего уровня и компонентов
"""

from tkinter import *
from tkinter.messagebox import *


def not_done():
    showerror("Not implemented", "Not available yet!")


def make_menu(parent):
    menu_bar = Frame(parent)                                        # создать Frame для строки меню
    menu_bar.pack(side=TOP, fill=X)

    f_button = Menubutton(menu_bar, text="File", underline=0)       # прикрепить Menubutton к Frame
    f_button.pack(side=LEFT)
    file = Menu(f_button)                                           # прикрепить Menu к Menubutton
    file.add_command(label="New...", command=not_done, underline=0)
    file.add_command(label="Open...", command=not_done, underline=0)
    file.add_command(label="Quit", command=parent.quit, underline=0)
    f_button.config(menu=file)                                      # связать кнопку и меню

    e_button = Menubutton(menu_bar, text="Edit", underline=0)
    e_button.pack(side=LEFT)
    edit = Menu(e_button)
    edit.add_command(label="Cut", command=not_done, underline=0)
    edit.add_command(label="Paste", command=not_done, underline=0)
    edit.add_separator()
    e_button.config(menu=edit)

    sub_menu = Menu(edit, tearoff=True)
    sub_menu.add_command(label="Spam", command=parent.quit, underline=0)
    sub_menu.add_command(label="Eggs", command=not_done, underline=0)
    edit.add_cascade(label="Stuff", menu=sub_menu, underline=0)

    return menu_bar


if __name__ == '__main__':
    root = Tk()
    root.title("Menu frame")
    make_menu(root)
    msg = Label(root, text="Frame menu basic")
    msg.pack(expand=YES, fill=BOTH)
    msg.config(relief=SUNKEN, width=40, height=7, bg='beige')
    root.mainloop()