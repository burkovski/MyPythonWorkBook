"""
то же самое, но с компоновкой по сетке и импортом с вызовом вместо
компоновки менеджером pack и командной строки; непосредственные вызовы
функций обычно выполняются быстрее, чем запуск файлов;
"""

from pract.Internet.Sockets.getfile import client
from tkinter import *
from tkinter.messagebox import showinfo


def on_submit():
    client(content["Host"].get(),
           int(content["Port"].get()),
           content["File"].get())
    showinfo("getfilegui2", "Download complete!")


root = Tk()
labels = ["Host", "Port", "File"]
content = {}
for row, label in enumerate(labels):
    Label(root, text=label).grid(row=row, column=0)
    entry = Entry(root)
    entry.grid(row=row, column=1)
    content[label] = entry

root.columnconfigure(0, weight=0)  # сделать растягиваемым
root.columnconfigure(1, weight=1)
Button(text="Submit", command=on_submit).grid(row=len(labels), column=0, columnspan=2)

root.title("getfilegui2")
root.bind("<Return>", lambda event: on_submit())
root.mainloop()
