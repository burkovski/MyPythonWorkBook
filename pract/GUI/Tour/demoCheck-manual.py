"""
флажки, сложный способ (без переменных)
"""

from tkinter import *

states = {k: False for k in range(10)}


def on_press(i):
    states[i] = not states[i]


root = Tk()
for i in range(10):
    Checkbutton(root, text=str(i), command=lambda ix=i: on_press(ix) or print(states)).pack(side=LEFT)

root.mainloop()
