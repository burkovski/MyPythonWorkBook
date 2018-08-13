from tkinter import *

gifdir = "../gifs/"
win = Tk()
img = PhotoImage(file=gifdir + "ora-pp.gif")
Button(win, image=img).pack()
win.mainloop()
