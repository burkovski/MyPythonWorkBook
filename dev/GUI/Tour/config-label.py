from tkinter import *


labelfont = ('times', 20, 'bold')       # семейство, размер, стиль

root = Tk()
widget = Label(root, text='Hello config world!')
widget.config(bg='black', fg='yellow')      # желтый текст на черном фоне
widget.config(font=labelfont)               # использовать увеличенный шрифт
widget.config(height=3, width=20)           # начальный размер: строк,символов
widget.pack(expand=YES, fill=BOTH)
root.mainloop()
