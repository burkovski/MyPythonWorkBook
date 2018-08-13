"""выводит диалог ввода параметров для сценария packer и запускает его"""

from glob import glob
from tkinter import *
from packer import pack
from formrows import make_formrow       # использовать инструмент создания форм


def pack_dialog():
    win = Toplevel()            # новое окно верхнего уровня с 2 фреймами-рядами + кнопка ok
    win.title("Enter Pack parameters")
    var1 = make_formrow(win, label="Qutput file")
    var2 = make_formrow(win, label="Files to pack", extend=True)
    Button(win, text="OK", command=win.destroy).pack()
    win.grab_set()
    win.focus_set()         # модальный: захватить мышь, фокус ввода, ждать закрытия окна диалога;
    win.wait_window()
    return var1.get(), var2.get()       # извлечь значения связанных переменных


def runPackDialog():
    output, patterns = pack_dialog()        # вывести диалог и ждать щелчка на кнопке ok или закрытия окна
    if output and patterns:                 # выполнить действия не связанные с графическим интерфейсом
        patterns = patterns.split()
        file_names = []
        for sublist in map(glob, patterns):     # вып. расширение шаблона вручную
            file_names.extend(sublist)
        print("Packer: {} {}".format(output, file_names))       # вывод также можно показать в графическом интерфейсе
        pack(ofile=output, ifiles=file_names)


if __name__ == "__main__":
    root = Tk()
    Button(root, text="Popup", command=runPackDialog).pack(fill=X)
    Button(root, text="Bye", command=root.quit).pack(fill=X)
    root.mainloop()
