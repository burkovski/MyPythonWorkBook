from tkinter import *


win1 = Toplevel()   # два независимых окна
win2 = Toplevel()   # являющихся частью одного и того же процесса

Button(win1, text='Spam', command=sys.exit).pack()
Button(win2, text='SPAM', command=sys.exit).pack()

Label(text='Popups').pack()     # по умолчанию добавляется в корневое окно Tk()

mainloop()
