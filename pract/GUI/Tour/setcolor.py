from tkinter import *
from tkinter.colorchooser import askcolor


def set_bg_color():
    triple, hexstr = askcolor()
    if hexstr:
        print(hexstr)
        push.config(bg=hexstr)


root = Tk()
push = Button(root, text='Set background color', command=set_bg_color)
push.config(height=3, font=('times', 20, 'bold'))
push.pack(expand=YES, fill=BOTH)
root.mainloop()
