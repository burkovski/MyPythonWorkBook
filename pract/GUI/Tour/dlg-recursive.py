from tkinter import *


def dialog():
    win = Toplevel()                                        # создать новое окно
    Label(win, text='Hard drive reformatted!').pack()       # добавить виджеты
    Button(win, text='OK', command=win.quit).pack()         # установить обр-к quit
    win.protocol("WM_DELETE_WINDOW", win.quit)              # завершить и при закрытии окна!

    win.focus_set()     # принять фокус ввода,
    win.grab_set()      # запретить доступ к др. окнам, пока открыт диалог
    win.mainloop()      # и запустить вложенный цикл обр. событий для ожидания
    win.destroy()

    print('dialog exit')


root = Tk()
Button(root, text='popup', command=dialog).pack()
root.mainloop()
