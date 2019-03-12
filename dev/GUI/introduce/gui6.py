from tkinter import *


class Hello(Frame):                     # расширенная версия класса Frame
    def __init__(self, parent=None):
        Frame.__init__(self, parent)    # вызвать метод __init__ суперкласса
        self.pack()
        self.data = 42
        self.make_widgets()             # прикрепить виджеты к себе

    def make_widgets(self):
        widget = Button(self, text="Hello frame world!", command=self.message)
        widget.pack(side=LEFT)

    def message(self):
        self.data += 1
        print("Hello frame world {0.data}".format(self))


if __name__ == '__main__':
    Hello().mainloop()
