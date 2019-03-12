from tkinter import *
import sys


def greeting():
    print("Hello stdout world!..")


win = Frame()
Button(win, text="Hello", command=greeting).pack(side=LEFT, fill=Y)
Label(win, text="Hello container world").pack(side=TOP)
Button(win, text="Quit", command=win.quit).pack(side=RIGHT, expand=YES, fill=X)

win.pack(expand=YES, fill=BOTH)
win.mainloop()