"""
создает формы с применением методов pack и grid в отдельных фреймах в одном
и том же окне; методы grid и pack не могут одновременно использоваться в одном
родительском контейнере (например, в корневом окне), но могут использоваться
в разных фреймах в одном и том же окне;
"""

from tkinter import *
from grid2 import grid_box, pack_box


boxes = (("Grid:", grid_box), ("Pack:", pack_box))
root = Tk()


for (label, box) in boxes:
    Label(root, text=label).pack()
    frame = Frame(root, bd=5, relief=RAISED)
    frame.pack(padx=5, pady=5)
    box(frame)

Button(root, text="Quit", command=root.quit).pack(fill=X)
root.mainloop()