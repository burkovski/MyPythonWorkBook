"""
реализует два набора инструментов, специфичных для типов
"""

from shellgui import *
from packdlg import runPackDialog
from unpackdlg import runUnpackDialog


class TextPack1(ListMenuGUI):
    def __init__(self):
        self.my_menu = [
            ("Pack  ", runPackDialog),
            ("Unpack", runUnpackDialog),
            ("Mtool ", self.not_done)
        ]
        ListMenuGUI.__init__(self)

    def for_toolbar(self, label):
        return label in {"Pack  ", "Unpack"}


class TextPack2(DictMenuGUI):
    def __init__(self):
        self.my_menu = {
            "Pack  ": runPackDialog,
            "Unpack": runUnpackDialog,
            "Mtool ": self.not_done
        }
        DictMenuGUI.__init__(self)


if __name__ == "__main__":
    from sys import argv
    if len(argv) > 1 and argv[1] == "list":
        print("list test")
        TextPack1().mainloop()
    else:
        print("dict test")
        TextPack2().mainloop()



