"""
отображает изображение с помощью альтернативного объекта из пакета PIL
поддерживает множество форматов изображений
"""

import os
import sys
from tkinter import *
from PIL.ImageTk import PhotoImage      # <== использовать альтернативный класс из
                                        # PIL, остальной программный код
                                        # без изменений

img_dir = sys.argv[1] if len(sys.argv) > 1 else "images"
img_file = "london-2010.jpg"
img_path = os.path.join(img_dir, img_file)
print(img_path)


root = Tk()
root.title(img_file)
img_obj = PhotoImage(file=img_path)
Label(root, image=img_obj).pack()
print(img_obj.width(), img_obj.height())
root.mainloop()
