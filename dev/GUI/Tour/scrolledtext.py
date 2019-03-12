"""
простой компонент просмотра текста или содержимого файла
"""

from tkinter import *


class ScrolledText(Frame):
    def __init__(self, parent=None, text="", file=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.make_widgets()
        self.set_text(text, file)

    def make_widgets(self):
        s_bar = Scrollbar(self)
        text = Text(self, relief=SUNKEN)
        s_bar.config(command=text.yview)
        text.config(yscrollcommand=s_bar.set)
        s_bar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, expand=YES, fill=BOTH)
        self.text = text

    def set_text(self, text, file):
        if file:
            text = open(file, 'r').read()
        self.text.delete("1.0", END)
        self.text.insert("1.0", text)
        self.text.mark_set(INSERT, "1.0")
        self.text.focus()

    def get_text(self):
        return "<{}>".format(self.text.get("1.0", END))


if __name__ == "__main__":
    root = Tk()
    if len(sys.argv) > 1:
        st = ScrolledText(file=sys.argv[1])
    else:
        st = ScrolledText(text="Words\ngo here")

    def show(event):
        print(repr(st.get_text()))

    root.bind("<Key-Escape>", show)
    root.mainloop()