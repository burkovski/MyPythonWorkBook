from tkinter import *

root = Tk()


rows = []
for i in range(5):
    cols = []
    for j in range(4):
        entry = Entry(root, relief=RIDGE)
        entry.grid(row=i, column=j, sticky=NSEW)
        entry.insert(END, "{}.{}".format(i, j))
        cols.append(entry)
    rows.append(cols)


def on_press():
    for row in rows:
        for col in row:
            print(col.get(), end=' ')
        print()


Button(root, text="Fetch!", command=on_press).grid(row=5, column=0, columnspan=2, sticky=EW)
Button(root, text="Quit!", command=root.quit).grid(row=5, column=2, columnspan=2, sticky=EW)
root.mainloop()
