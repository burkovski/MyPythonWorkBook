from tkinter import *


colors = ["red", "green", "orange", "white", "yellow", "blue"]

for row, color in enumerate(colors):
    Label(text=color.capitalize(), relief=RIDGE, width=25).grid(row=row, column=0)
    Entry(bg=color, relief=SUNKEN, width=50). grid(row=row, column=1)

mainloop()
