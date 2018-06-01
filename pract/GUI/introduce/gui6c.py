from tkinter import *
from gui6 import Hello


class HelloContainer(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        self.make_widgets()

    def make_widgets(self):
        Hello(self).pack(side=RIGHT)
        Button(self, text="Attach", command=self.quit).pack(side=LEFT)


if __name__ == '__main__':
    HelloContainer().mainloop()