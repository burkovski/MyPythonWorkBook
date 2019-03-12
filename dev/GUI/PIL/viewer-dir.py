"""
выводит все изображения, найденные в каталоге, открывая новые окна
GIF-файлы поддерживаются стандартными средствами tkinter, но JPEG-файлы будут
пропускаться при отсутствии пакета PIL
"""

import os
import sys
from tkinter import *
from PIL.ImageTk import PhotoImage      # <== требуется для JPEG и др. формато

img_dir = sys.argv[1] if len(sys.argv) > 1 else "images"
img_files = os.listdir(img_dir)


root = Tk()
root.title('Viewer')
quit = Button(
    root,
    text="Quit all",
    command=root.quit,
    font=('courier', 25)
)
quit.pack()
save_photos = []

for img_file in img_files:
    img_path = os.path.join(img_dir, img_file)
    popup = Toplevel()
    popup.title(img_file)
    try:
        img_obj = PhotoImage(file=img_path)
        Label(root, image=img_obj).pack()
        print(img_path, img_obj.width(), img_obj.height())
        save_photos.append(img_obj)
    except Exception:
        err_msg = "skipping {}\n{}".format(img_file, sys.exc_info()[1])
        Label(popup, text=err_msg).pack()

root.mainloop()