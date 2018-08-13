"""
переключатели, сложный способ (без переменных)
обратите внимание, что метод deselect переключателя просто устанавливает пустую
строку в качестве его значения, поэтому нам по-прежнему требуется присвоить
переключателям уникальные значения или использовать флажки;
"""

from tkinter import *

state = ''
buttons = []


def on_press(ix):
    global state
    state = ix
    for btn in buttons:
        btn.deselect()
    buttons[ix].select()


root = Tk()
for ix in range(10):
    rd = Radiobutton(
        root,
        text=str(ix),
        value=str(ix),
        command=lambda i=ix: on_press(i)
    )
    rd.pack(side=LEFT)
    buttons.append(rd)


root.mainloop()
print(state)
