from tkinter import *
import sys


def hello(event):
    print("Press twice to exit")        # одиночный щелчок левой кнопкой


def quit(event):                        # двойной щелчок левой кнопкой
    print("Hello, I must going...")     # event дает виджет, координаты и т.д.
    sys.exit()


widget = Button(text="Hello event world")
widget.pack()
widget.bind("<Button-1>", hello)        # привязать обработчик щелчка
widget.bind("<Double-1>", quit)         # привязать обработчик двойного щелчка
widget.mainloop()
