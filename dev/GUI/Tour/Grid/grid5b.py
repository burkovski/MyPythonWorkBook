"""
добавляет суммирование по столбцам и очистку полей ввода
"""

from tkinter import *

root = Tk()
num_row, num_col = 5, 4
rows = []
sums = []

for row in range(num_row):
    cols = []
    for col in range(num_col):
        entry = Entry(root, relief=RIDGE)
        entry.grid(row=row, column=col)
        entry.insert(END, "{}.{}".format(row, col))
        cols.append(entry)
    rows.append(cols)

for col in range(num_col):
    label = Label(text='?', relief=SUNKEN)
    label.grid(row=num_row, column=col, sticky=NSEW)
    sums.append(label)


def on_print():
    for row in rows:
        for col in row:
            print(col.get(), end=' ')
        print()
    print()


def on_sum():
    tots = [0 for _ in range(num_col)]
    for col in range(num_col):
        for row in range(num_row):
            tots[col] += eval(rows[row][col].get())
    for col in range(num_col):
        sums[col].config(text=str(tots[col]))


def on_clear():
    for row in rows:
        for col in row:
            col.delete('0', END)
            col.insert(END, "0.0")
    for sum in sums:
        sum.config(text='?')


buttons = (("Sum", on_sum), ("Print", on_print), ("Clear", on_clear), ("Quit", sys.exit))
for col, (text, command) in enumerate(buttons):
    Button(text=text, command=command).grid(row=num_row+1, column=col)
mainloop()
