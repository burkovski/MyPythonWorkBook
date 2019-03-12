"""
простой настраиваемый компонент окна списка с прокруткой
"""

from tkinter import *


class ScrolledList(Frame):
    def __init__(self, options, parent=None, **kwargs):
        Frame.__init__(self, parent, **kwargs)
        self.pack(expand=YES, fill=BOTH)        # сделать растягиваемым
        self.make_widgets(options)

    def handle_list(self, event):
        # index = self.listbox.curselection()     # при двойном щелчке на списке
        # label = self.listbox.get(index)         # извлечь выбранный текст
        # self.run_command(label)                 # и вызвать действие или get(ACTIVE)
        for ix in self.listbox.curselection():
            self.run_command(self.listbox.get(ix))

    def make_widgets(self, options):
        s_bar = Scrollbar(self)
        s_list = Listbox(self)
        s_bar.config(command=s_list.yview)          # связать s_bar и s_list
        s_list.config(yscrollcommand=s_bar.set)     # сдвиг одного = сдвиг другого
        s_bar.pack(side=RIGHT, fill=Y)              # первым добавлен – посл. обрезан
        s_list.pack(side=LEFT, expand=YES, fill=BOTH)   # список обрезается первым
        for label in options:               # или enumerate(options)
            s_list.insert(END, label)       # добавить в виджет списка
        s_list.config(selectmode=EXTENDED, setgrid=1)       # режимы выбора, измен. разм.
        s_list.bind("<Double-1>", self.handle_list)         # установить обр-к события
        s_list.bind("<Return>", self.handle_list)         # установить обр-к события
        self.listbox = s_list

    def run_command(self, selection):
        print("You selected: <{}>".format(selection))


if __name__ == "__main__":
    options = map(lambda x: "Lumberjack-{}".format(x), range(20))
    ScrolledList(options).mainloop()
