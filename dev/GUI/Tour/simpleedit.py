"""
за счет наследования добавляет в ScrolledText типичные инструменты
редактирования; аналогичного результата можно было бы добиться, применив прием
композиции (встраивания); ненадежно! -- надмножество функций имеется в PyEdit;
"""

from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename
from quitter import Quitter
from scrolledtext import ScrolledText


class SimpleEditor(ScrolledText):
    def __init__(self, parent=None, file=None):
        frame = Frame(parent)
        frame.pack(fill=X)
        Button(frame, text="Save", command=self.on_save).pack(side=LEFT)
        Button(frame, text="Cut", command=self.on_cut).pack(side=LEFT)
        Button(frame, text="Paste", command=self.on_paste).pack(side=LEFT)
        Button(frame, text="Find", command=self.on_find).pack(side=LEFT)
        Quitter(frame).pack(side=LEFT)
        ScrolledText.__init__(self, parent, file=file)
        self.text.config(font=("courier", 9, "normal"))

    def on_save(self):
        file_name = asksaveasfilename()
        if file_name:
            all_text = self.get_text()                  # от начала до конца
            open(file_name, 'w').write(all_text)        # сохранить текст в файл

    def on_cut(self):
        try:
            text = self.text.get(SEL_FIRST, SEL_LAST)
            self.text.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()                      # очистить буфер
            self.clipboard_append(text)                 # сохранить строку текста
        except TclError:
            pass

    def on_paste(self):
        try:
            text = self.selection_get(selection="CLIPBOARD")        # добавляет текст из буфера
            self.text.insert(INSERT, text)
        except TclError:
            pass                    # не вставлять

    def on_find(self):
        target = askstring("Simple Editor", "Search string?")
        if target:
            where = self.text.search(target, INSERT, END)           # от позиции курсора вернуть индекс
            if where:
                print(where)
                past_it = where + "+{0}c".format(len(target))       # индекс за целью
                self.text.tag_remove(SEL, "1.0", END)               # снять выделение
                self.text.tag_add(SEL, where, past_it)              # выделить найденное
                self.text.mark_set(INSERT, past_it)                 # установить метку вставки
                self.text.see(INSERT)                               # прокрутить текст
                self.text.focus()  # выбрать виджет Text


if __name__ == "__main__":
    if len(sys.argv) > 1:
        SimpleEditor(file=sys.argv[1]).mainloop()                   # имя файла в ком. строке
    else:
        SimpleEditor(file="simpleedit.py").mainloop()               # или нет: пустой виджет
