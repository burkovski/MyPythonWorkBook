"""
реализация графического интерфейса - объединяет GuiMaker, GuiMixin и данный
класс
"""

import os
from tkinter import *
from guimaker import *
from guimixin import *


class Hello(GuiMixin, GuiMakerWindowMenu):
    def start(self):
        self.hellos = 0
        self.master.title("Gui Maker Demo")

        def spawn_me():
            self.spawn("big_gui.py")

        self.menubar = [
            ("File", 0, [
                ("New...", 0, spawn_me),
                ("Open...", 0, self.file_open),
                ("Quit...", 0, self.quit)
            ]),

            ("Edit", 0, [
                ("Cut", -1, self.not_done),
                ("Paste", -1, self.not_done),
                "separator",
                ("Stuff", -1, [
                    ("Clone", -1, self.clone),
                    ("More", -1, self.more)
                ]),
                ("Delete", -1, lambda: 0)
            ]),

            ("Play", 0, [
                ("Hello", 0, self.greeting),
                ("Popup...", 0, self.dialog),
                ("Demos", 0, [
                    ("Toplevels", 0, lambda: self.spawn("../Tour/toplevel2.py")),
                    ("Frames", 0, lambda: self.spawn("../Tour/demoAll-frames.py")),
                    ("Images", 0, lambda: self.spawn("../Tour/buttonpics.py")),
                    ("Alarm", 0, lambda: self.spawn("../Tour/alarm.py", wait=False)),
                    ("Other", -1, self.pick_demo)
                ])
            ])
        ]

        self.toolbar = [
            ("Quit", self.quit, {"side": RIGHT}),
            ("Hello", self.greeting, {"side": LEFT}),
            ("Popup", self.dialog, {"side": LEFT, "expand": YES})
        ]

    def make_widgets(self):
        middle = Label(self,
                       text="Hello maker world!",
                       width=40, height=10,
                       relief=SUNKEN, cursor="pencil", bg="white")
        middle.pack(expand=YES, fill=BOTH)

    def greeting(self):
        self.hellos += 1
        if self.hellos % 3:
            print("Hi!")
        else:
            self.infobox("Three", "HELLO!")

    def dialog(self):
        button = self.question(
            "OOPS!",
            "You typed \"rm*\" ... continue?",
            "questhead", ("yes", "no"))
        if button:
            self.quit()

    def file_open(self):
        pick = self.selectOpenFile(file="big_gui.py")
        if pick:
            self.browser(pick)

    def more(self):
        new = Toplevel()
        Label(new, text="A new non-modal window").pack()
        Button(new, text="More", command=self.more).pack(side=LEFT)
        Button(new, text="Quit", command=new.destroy).pack(side=RIGHT)

    def pick_demo(self):
        pick = self.selectOpenFile(dir='..')
        if pick:
            self.spawn(pick)


if __name__ == "__main__":
    Hello().mainloop()
