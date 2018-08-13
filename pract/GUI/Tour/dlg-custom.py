from tkinter import *

makemodal = len(sys.argv) > 1


def dialog():
    win = Toplevel()                                        # создать новое окно
    Label(win, text='Hard drive reformatted!').pack()       # добавить виджеты
    Button(win, text='OK', command=win.destroy).pack()      # установить обработчик
    if makemodal:
        win.focus_set()         # принять фокус ввода,
        win.grab_set()          # запретить доступ к др. окнам, пока открыт диалог
        win.wait_window()       # ждать, пока win не будет уничтожен
    print('dialog exit')        # иначе – сразу вернуть управление


root = Tk()
Button(root, text='popup', command=dialog).pack()
root.mainloop()
