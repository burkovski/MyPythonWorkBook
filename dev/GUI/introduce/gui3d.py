from tkinter import *
import sys


class HelloCallable:
    def __init__(self):     # __init__ вызывается при создании объекта
        self.msg = "Hello __call__ world"

    def __call__(self):
        print(self.msg)     # __call__ вызывается при попытке обратиться
        sys.exit()          # к объекту класса как к функции


widget = Button(None, text="Hello event world", command=HelloCallable())
widget.pack()
widget.mainloop()
