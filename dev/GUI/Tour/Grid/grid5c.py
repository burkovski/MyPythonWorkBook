"""
релизация в виде встраеваемого класса
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from quitter import Quitter


class SumGrid(Frame):
    def __init__(self, parent=None, num_row=5, num_col=5):
        Frame.__init__(self, parent)
        self.num_row = num_row
        self.num_col = num_col
        self.rows = []
        self.sums = []
        self.buttons = (
            ("Sum", self.on_sum),
            ("Print", self.on_print),
            ("Clear", self.on_clear),
            ("Load", self.on_load),
        )
        self.make_widgets()

    def make_widgets(self):
        print(self.num_row, self.num_col)
        self.rows.clear()
        self.sums.clear()

        for i in range(self.num_row):
            cols = []
            for j in range(self.num_col):
                entry = Entry(self, relief=RIDGE)
                entry.grid(row=i+1, column=j, sticky=NSEW)
                entry.insert(END, "{}.{}".format(i, j))
                cols.append(entry)
                self.columnconfigure(j, weight=1)
            self.rowconfigure(i+1, weight=1)
            self.rows.append(cols)

        for i in range(self.num_col):
            label = Label(self, text='?', relief=SUNKEN)
            label.grid(row=self.num_row+1, column=i, sticky=NSEW)
            self.sums.append(label)

        for (column, (text, command)) in enumerate(self.buttons):
            Button(self, text=text, command=command).grid(row=0, column=column, sticky=NSEW)
        Quitter(self).grid(row=0, column=len(self.buttons), sticky=NSEW)

    def on_sum(self):
        tots = [0 for _ in range(self.num_col)]
        for row in self.rows:
            for ix, field in enumerate(row):
                tots[ix] += eval(field.get())

        for ix in range(self.num_col):
            self.sums[ix].config(text=str(tots[ix]))

    def on_print(self):
        for row in self.rows:
            for col in row:
                print(col.get(), end=' ')
            print()
        print()

    def on_clear(self):
        for row in self.rows:
            for col in row:
                col.delete('0', END)
                col.insert(END, '0.0')
        for field in self.sums:
            field.config(text='?')

    def on_load(self):
        file = askopenfilename()
        if file:
            for row in self.rows:
                for col in row:
                    col.grid_forget()       # очистить интерфейс
            for sum in self.sums:
                sum.grid_forget()

            file_lines = open(file, 'r').readlines()   # загрузить данные
            self.num_row = len(file_lines)
            self.num_col = len(file_lines[0].split())       # изменить размер табл.
            self.make_widgets()

            for (row, line) in enumerate(file_lines):
                fields = line.split()
                for (column, field) in enumerate(fields):
                    self.rows[row][column].delete('0', END)
                    self.rows[row][column].insert(END, field)


if __name__ == "__main__":
    root = Tk()
    root.title("Summer Grid")
    if len(sys.argv) == 3:
        rows, cols = sys.argv[1:]
        SumGrid(root, rows, cols).pack(expand=YES, fill=BOTH)
    else:
        SumGrid(root).pack(expand=YES, fill=BOTH)
    root.mainloop()
