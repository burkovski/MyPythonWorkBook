from tkinter import *


for i in range(5):
    for j in range(4):
        label = Label(text="{}.{}".format(i, j), relief=RIDGE)
        label.grid(row=i, column=j)

mainloop()
