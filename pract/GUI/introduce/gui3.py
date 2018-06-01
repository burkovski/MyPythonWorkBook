import sys
from tkinter import *


def quit_func():
    print("Hello, I must be going...")
    sys.exit()


widget = Button(None, text="Hello event world", command=quit_func)
widget.pack()
widget.mainloop()
