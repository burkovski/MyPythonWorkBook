"""
то же, что и viewer_thumbs, но использует менеджер компоновки grid, чтобы
добиться более стройного размещения миниатюр; того же эффекта можно добиться
с применением фреймов и менеджера pack, если кнопки будут иметь фиксированный
и одинаковый размер;
использует кнопки фиксированного размера для миниатюр, благодаря чему
достигается еще более стройное размещение; размеры определяются по объектам
изображений, при этом предполагается, что для всех миниатюр был установлен один
и тот же максимальный размер; по сути именно это и делают графические интерфейсы
файловых менеджеров;
"""

from tkinter import *
import sys
import math
from PIL.ImageTk import PhotoImage
from viewer_thumbs import make_thumbs, ViewOne


def viewer(img_dir, kind=Toplevel, cols=None):
    """
    измененная версия, размещает миниатюры по сетке
    """
    win = kind()
    win.title('Viewer: ' + img_dir)
    thumbs = make_thumbs(img_dir)
    if not cols:
        cols = int(math.ceil(math.sqrt(len(thumbs))))  # fixed or N x N

    row_num = 0
    save_photos = []
    while thumbs:
        thumbs_row, thumbs = thumbs[:cols], thumbs[cols:]
        colnum = 0
        for (img_file, img_obj) in thumbs_row:
            size = max(img_obj.size)        # ширина, высота
            photo = PhotoImage(img_obj)
            link = Button(win, image=photo)
            handler = lambda save_file=img_file: ViewOne(img_dir, save_file)
            link.config(command=handler, width=size, height=size)
            link.grid(row=row_num, column=colnum)
            save_photos.append(photo)
            colnum += 1
        row_num += 1

    Button(win, text='Quit', command=win.quit).grid(columnspan=cols, stick=EW)
    return win, save_photos


if __name__ == '__main__':
    img_dir = sys.argv[1] if len(sys.argv) > 1 else 'images'
    main, save = viewer(img_dir, kind=Tk)
    main.mainloop()
