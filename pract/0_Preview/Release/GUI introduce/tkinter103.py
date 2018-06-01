from tkinter import *
from tkinter102 import MyGui

# главное окно приложения
mainwin = Tk()
Label(mainwin, text=__name__).pack()

# окно диалога
popup = Toplevel()
Label(popup, text='Attach').pack(side=LEFT)
MyGui(popup).pack()
mainwin.mainloop()