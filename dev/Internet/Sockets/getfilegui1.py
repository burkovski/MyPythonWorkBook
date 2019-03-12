"""
запускает сценарий getfile в режиме клиента из простого
графического интерфейса на основе tkinter;
точно так же можно было бы использовать os.fork+exec, os.spawnv
(смотрите модуль Launcher);
в windows: замените 'python' на 'start', если каталог
с интерпретатором не перечислен в переменной окружения PATH;
"""

import sys
import os
from tkinter import *
from tkinter.messagebox import showinfo


def on_return_key():
    cmd_line = "python getfile.py -mode client"
    for (cmd_key, value) in content.values():
        cmd_value = value.get()
        if cmd_value:
            cmd_line += " -{} {}".format(cmd_key, cmd_value)
    os.system(cmd_line)
    showinfo("getfilegui1", "Download complete")


box = Tk()
labels = ["Host", "Port", "File"]
content = {}
for label in labels:
    row = Frame(box)
    row.pack(fill=X)
    Label(row, text=label, width=6).pack(side=LEFT)
    entry = Entry(row)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    content[label] = (label.lower(), entry)
print(content)

box.title("getfilegui1")
box.bind("<Return>", lambda event: on_return_key())
box.mainloop()
