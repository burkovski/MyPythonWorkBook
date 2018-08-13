"""
демонстрация основных возможностей холста
"""

from tkinter import *


canvas = Canvas(width=525, height=300, bg="white")      # 0,0 - верхний левый угол
canvas.pack(expand=YES, fill=BOTH)                      # рост вниз и вправо

canvas.create_line(100, 100, 200, 200)      # fromX, fromY, toX, toY
canvas.create_line(100, 200, 200, 300)

for i in range(1, 20, 2):
    canvas.create_line(0, i, 50, i)

canvas.create_oval(10, 10, 200, 200, width=0, fill="blue")
canvas.create_arc(200, 200, 300, 100)
canvas.create_rectangle(200, 200, 300, 300, width=5, fill="red")
canvas.create_line(0, 300, 150, 150, width=10, fill="green")

img = PhotoImage(file="../../gifs/ora-lp4e.gif")
canvas.create_image(325, 25, image=img, anchor=NW)      # встроить изображение

widget = Label(canvas, text="SPAM!", fg="white", bg="black")
widget.pack()

canvas.create_window(100, 100, window=widget)           # встроить виджет
canvas.create_text(100, 280, text="Ham")                # нарисовать текст

mainloop()
