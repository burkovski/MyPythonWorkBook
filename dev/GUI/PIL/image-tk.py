"""
отображает изображение с помощью стандартного объекта PhotoImage из биб­
лиотеки tkinter; данная реализация может работать с GIF-файлами, но не может
обрабатывать изображения в формате JPEG; использует файл с изображением, имя
которого указано в командной строке, или файл по умолчанию; используйте Canvas
вместо Label, чтобы обеспечить возможность прокрутки, и т.д.
"""

import os
import sys
from tkinter import *

img_dir = sys.argv[1] if len(sys.argv) > 1 else "images"
img_file = "london-2010.gif"
img_path = os.path.join(img_dir, img_file)
print(img_path)


root = Tk()
root.title(img_file)
img_obj = PhotoImage(file=img_path)
Label(root, image=img_obj).pack()
print(img_obj.width(), img_obj.height())
root.mainloop()
