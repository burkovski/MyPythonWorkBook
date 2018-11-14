from tkinter import *
from tkinter.messagebox import showerror
import shelve
db_name = "class-shelve"
field_names = ("name", "age", "job", "pay")

def makeWidgets():
    global entries
    window = Tk()
    window.title("People Shelve")
    form = Frame(window)
    form.pack()
    entries = {}
    for (ix, label) in enumerate(("key", ) + field_names):
        lab = Label(form, text=label)
        ent = Entry(form)
        lab.grid(row=ix, column=0)
        ent.grid(row=ix, column=1)
        entries[label] = ent
    Button(window, text="Fetch", command=fetchRecord).pack(side=LEFT)
    Button(window, text="Update", command=updateRecord).pack(side=LEFT)
    Button(window, text="Quit", command=window.quit).pack(side=RIGHT)
    return window

def fetchRecord():
    key = entries['key'].get()
    try:
        record = db[key]
    except KeyError:
        showerror(title="Error!", message="No such key!")
    else:
        for field in field_names:
            entries[field].delete(0, END)
            entries[field].insert(0, repr(getattr(record, field)))

def updateRecord():
    print(entries)
    key = entries['key'].get()
    if key in db:
        record = db[key]
    else:
        from initdata import Person
        record = Person(name='?', age='?')
    for field in field_names:
        setattr(record, field, eval(entries[field].get()))
    db[key] = record

db = shelve.open(db_name)
window = makeWidgets()
window.mainloop()
db.close()