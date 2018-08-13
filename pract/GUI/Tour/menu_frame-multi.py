from tkinter import *
from menu_frame import make_menu


root = Tk()
for _ in range(2):
    menu = make_menu(root)
    menu.config(bd=2, relief=RAISED)
    Label(root, bg="black", width=25, height=5).pack(expand=YES, fill=BOTH)
Button(root, text="Quit", command=root.quit).pack(side=BOTTOM, fill=X)
root.mainloop()
