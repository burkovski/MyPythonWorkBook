"""
классы панелей флажков и переключателей для приложений, которые запрашивают
информацию о состоянии позднее;
передается список вариантов выбора, вызывается метод state(), работа
с переменными выполняется автоматически
"""

from tkinter import *


class CheckBar(Frame):
    def __init__(self, parent=None, picks=None, side=LEFT, anchor=W, **kwargs):
        super(CheckBar, self).__init__(parent, **kwargs)
        self.vars = []
        if picks:
            for pick in picks:
                var = IntVar()
                ch_button = Checkbutton(self, text=pick, variable=var)
                ch_button.pack(side=side, anchor=anchor, expand=YES)
                self.vars.append(var)

    def state(self):
        return [var.get() for var in self.vars]


class RadioBar(Frame):
    def __init__(self, parent=None, picks=None, side=LEFT, anchor=W, **kwargs):
        super(RadioBar, self).__init__(parent, **kwargs)
        self.var = StringVar()
        if picks:
            self.var.set(picks[0])
            for pick in picks:
                rd_button = Radiobutton(parent, text=pick, value=pick, variable=self.var)
                rd_button.pack(side=side, anchor=anchor, expand=YES)

    def state(self):
        return self.var.get()


if __name__ == "__main__":
    def on_all(self):
        for var in self.vars:
            var.set(1)


    root = Tk()
    lng = CheckBar(root, ['Python', 'C#', 'Java', 'C++'])
    gui = RadioBar(root, ['win', 'x11', 'mac'], side=TOP, anchor=NW)
    tgl = CheckBar(root, ['All'])

    gui.pack(side=LEFT, fill=Y)
    lng.pack(side=TOP, fill=X)
    tgl.pack(side=LEFT)
    lng.config(relief=GROOVE, bd=2)
    gui.config(relief=GROOVE, bd=2)


    def all_states():
        print(gui.state(), lng.state(), tgl.state())


    from quitter import Quitter

    Quitter(root).pack(side=RIGHT)
    Button(root, text="Peek", command=all_states).pack(side=RIGHT)
    root.mainloop()
