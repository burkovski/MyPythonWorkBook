from tkinter import *

gifdir ="../gifs/"

win = Tk()
img = PhotoImage(file=gifdir + "ora-lp4e.gif")
cnvs = Canvas(win)
cnvs.pack(fill=BOTH)
cnvs.config(width=img.width(), height=img.height())
cnvs.create_image(2, 2, image=img, anchor=NW)
win.mainloop()
