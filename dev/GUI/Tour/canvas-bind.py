"""
привязка обработчиков событий к холсту и к элементам на нем
"""

from tkinter import *


def on_canvas_click(event):
    print("Got canvas click at: [x={0.x}, y={0.y}, widget={0.widget}]".format(event))


def on_obj_click(event):
    print("Got object click at: [x={0.x}, y={0.y}, widget={0.widget}]".format(event), end=' ')
    print(event.widget.find_closest(event.x, event.y))          # найти ID текстового объекта


root = Tk()
canvas = Canvas(root, width=300, height=300)
obj1 = canvas.create_text(150, 100, text="Click me one!")
obj2 = canvas.create_text(150, 200, text="Click me two!")
canvas.bind("<Double-1>", on_canvas_click)                      # привязать к самому холсту
canvas.tag_bind(obj1, "<Double-1>", on_obj_click)               # привязать к элементу
canvas.tag_bind(obj2, "<Double-1>", on_obj_click)               # теги тоже можно использовать
canvas.pack()
root.mainloop()
