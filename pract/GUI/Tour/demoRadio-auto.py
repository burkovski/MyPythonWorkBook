"""
переключатели, простой способ
"""

from tkinter import *


root = Tk()
var = StringVar()
for i in range(10):
    Radiobutton(root, text=str(i), variable=var, value=i).pack(side=LEFT)

root.mainloop()
print(var.get())
