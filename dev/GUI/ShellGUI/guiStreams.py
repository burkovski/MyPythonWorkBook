"""
##############################################################################
начальная реализация классов, похожих на файлы, которые можно использовать для
перенаправления потоков ввода и вывода в графические интерфейсы; входные данные
поступают из стандартного диалога (единый интерфейс вывод+ввод или постоянное
поле Entry для ввода были бы удобнее); кроме того, некорректно берутся строки
в запросах входных данных, когда количество байтов > len(строки); в GuiInput
можно было бы добавить методы __iter__/__next__, для поддержки итераций по
строкам, как в файлах, но это способствовало бы порождению большого количества
всплывающих окон;
##############################################################################
"""

from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.scrolledtext import ScrolledText


class GuiOutput:
    font = ("courier", 9, "normal")
    def __init__(self, parent=None):
        self.text = None
        if parent:
            self.popup_now(parent)          # сейчас или при первой записи

    def popup_now(self, parent=None):       # сейчас в родителе, Toplevel потом
        if self.text:
            return
        self.text = ScrolledText(parent or Toplevel())
        self.text.config(font=self.font)
        self.text.pack()

    def write(self, text):
        self.popup_now()
        self.text.insert(END, str(text))
        self.text.see(END)
        self.text.update()                  # обновлять после каждой строки

    def writelines(self, lines):            # строки уже включают '\n'
        for line in lines:
            self.write(line)


class GuiInput:
    def __init__(self):
        self.buff = ''

    @staticmethod
    def input_line():
        line = askstring("Gui Input", "Enter input line + <crlf> (cancel=eof)")
        if line:
            return "{}\n".format(line)
        else:
            return ''

    def read(self, bytes=None):
        if not self.buff:
            self.input_line()
        if bytes:
            text = self.buff[:bytes]
            self.buff = self.buff[bytes:]
        else:
            text = ''
            line = self.buff
            while line:
                text = "{}{}".format(text, line)
                line = self.input_line()
        return text

    def readline(self):
        text = self.buff or self.input_line()
        self.buff = ''
        return text

    def readlines(self):
        lines = []
        while True:
            next = self.readline()
            if not next:
                break
            lines.append(next)
        return lines


def redirectedGuiFunc(func, *args, **kwargs):
    import sys
    saved_streams = sys.stdin, sys.stdout
    sys.stdin = GuiInput()
    sys.stdout = GuiOutput()
    sys.stderr = sys.stdout
    result = func(*args, **kwargs)
    sys.stdin, sys.stdout = saved_streams
    return result


def redirectedGuiShellCmd(command):
    import os
    input = os.popen(command)
    output = GuiOutput()
    def reader(input, output):
        while True:
            line = input.readline()
            if not line: break
            output.write(line)
    reader(input, output)


if __name__ == "__main__":
    def make_upper():
        while True:
            try:
                line = input("Line? ")
            except Exception:
                break
            print(line.upper())
        print("<EOF>")

    def make_lower(input, output):
        while True:
            line = input.readline()
            if not line: break
            output.write(line.lower())
        print("<EOF>")

    root = Tk()
    buttons = (
        ("Test streams", lambda: redirectedGuiFunc(make_upper)),
        ("Test files", lambda: make_lower(GuiInput(), GuiOutput())),
        ("Test popen", lambda: redirectedGuiShellCmd("dir *")),
    )
    for (text, command) in buttons:
        Button(root, text=text, command=command).pack(fill=X)
    root.mainloop()
