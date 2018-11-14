"""
модуль windows должен импортироваться, иначе атрибут __name__ будет иметь
значение __main__ в функции findIcon
"""

from tkinter import Button, mainloop
from windows import MainWindow, PopupWindow, ComponentWindow


def _selftest():
    class Content:
        def __init__(self):
            Button(self, text="Larch", command=self.quit).pack()
            Button(self, text="Sing", command=self.destroy).pack()

    class ContentMix(MainWindow, Content):
        def __init__(self):
            MainWindow.__init__(self, "Mixin", "Main")
            Content.__init__(self)
    ContentMix()

    class ContentMix(PopupWindow, Content):
        def __init__(self):
            PopupWindow.__init__(self, "Mixin", "Popup")
            Content.__init__(self)
    prev = ContentMix()

    class ContentMix(ComponentWindow, Content):
        def __init__(self):
            ComponentWindow.__init__(self, prev)
            Content.__init__(self)
    ContentMix()

    class ContentSub(PopupWindow):
        def __init__(self):
            PopupWindow.__init__(self, "Popup", "Subclass")
            Button(self, text="Pine", command=self.quit).pack()
            Button(self, text="Sing", command=self.destroy).pack()
    ContentSub()

    win = PopupWindow("Popup", "Attachment")
    Button(win, text="Redwood", command=win.quit).pack()
    Button(win, text="Sing", command=win.destroy).pack()

    mainloop()


if __name__ == "__main__":
    _selftest()
