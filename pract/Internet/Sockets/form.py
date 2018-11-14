"""
##################################################################
многократно используемый класс формы, задействованный
в сценарии getfilegui (и в других)
##################################################################
"""

from tkinter import *


class Form:                                                     # немодальное окно формы
    def __init__(self, labels, parent=None):                    # передать список меток полей
        self.entry_size = 40
        self.label_size = max(len(x) for x in labels) + 2
        box = Frame(parent)                         # в окне есть ряды, кнопка
        box.pack(expand=YES, fill=BOTH)             # ряды оформлены, как фреймы
        rows = Frame(box, bd=2, relief=GROOVE)      # нажатие кнопки или Enter
        rows.pack(side=TOP, expand=YES, fill=X)     # вызывают метод on_submit
        self.content = {}
        for label in labels:
            row = Frame(rows)
            row.pack(fill=X)
            Label(row, text=label, width=self.label_size).pack(side=LEFT)
            entry = Entry(row, width=self.entry_size)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            self.content[label] = entry
        Button(box, text="Cancel", command=self.on_cancel).pack(side=RIGHT)
        Button(box, text="Submit", command=self.on_submit).pack(side=RIGHT)
        box.master.bind("<Return>", lambda event: self.on_submit())
        self.box = box

    def on_submit(self):            # переопределить этот метод в подклассах
        for key in self.content:
            print(key, '\t=>\t', self.content[key].get().lstrip())

    def on_cancel(self):            # переопределить этот метод в подклассах
        self.box.master.quit()


class DynamicForm(Form):
    def __init__(self, labels=None, parent=None):
        labels = input("Enter field names: ").split()
        super(DynamicForm, self).__init__(labels, parent)

    def on_submit(self):
        print("Field values...")
        super(DynamicForm, self).on_submit()
        self.on_cancel()


if __name__ == "__main__":
    import sys
    root = Tk()
    if len(sys.argv) == 1:
        Form(["Name", "Age", "Job"], root)        # предопределенные поля остаются после передачи
    else:
        DynamicForm(root)                       # динамически созданные поля ичезают
    root.mainloop()
