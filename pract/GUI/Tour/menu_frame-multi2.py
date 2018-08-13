from tkinter import *
from menu_frame import make_menu


root = Tk()
for _ in range(3):          # три меню, вложенные в контейнеры
    frame = Frame(root)
    menu = make_menu(frame)
    menu.config(bd=2, relief=RAISED)
    frame.pack(expand=YES, fill=BOTH)
    Label(frame, bg="black", width=25, height=5).pack(expand=YES, fill=BOTH)
Button(root, text="Quit", command=root.quit).pack(side=BOTTOM, fill=X)
root.mainloop()
