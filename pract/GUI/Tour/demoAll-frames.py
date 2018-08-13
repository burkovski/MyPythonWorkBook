"""
4 класса демонстрационных компонентов (вложенных фреймов) в одном окне;
в одном окне присутствуют также 5 кнопок Quitter, причем щелчок на любой из
них приводит к завершению программы; графические интерфейсы могут повторно
использоваться, как фреймы в контейнере, независимые окна или процессы;
"""
from tkinter import *
from quitter import Quitter

demo_modules = ["demoDlg", "demoCheck", "demoRadio", "demoScale"]
parts = []


def add_components(root):
    for demo in demo_modules:
        module = __import__(demo)                       # импортировать по имени в виде строки
        part = module.Demo(root, bd=2, relief=GROOVE)   # прикрепить экземпляр
        part.pack(side=LEFT, expand=YES, fill=BOTH)     # растягивать вместе с окном
        parts.append(part)                              # добавить в список


def dump_state():
    for part in parts:
        print(part.__module__ + ':', end=' ')
        if hasattr(part, 'report'):     # вызвать метод report, если имеется
            part.report()
        else:
            print('none')


root = Tk()
root.title("Frames")
Label(root, text="Multiple Frame Demo", bg="white").pack()
Button(root, text="State", command=dump_state).pack(fill=X)
Quitter(root).pack(fill=X)
add_components(root)
root.mainloop()
