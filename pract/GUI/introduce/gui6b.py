from tkinter import *
from sys import exit
from gui6 import Hello


parent = Frame()    # создать контейнерный виджет
parent.pack()
Hello(parent).pack(side=RIGHT)  # прикрепить виджет Hello, не запуская его

Button(parent, text="Attach", command=exit).pack(side=LEFT)
parent.mainloop()
