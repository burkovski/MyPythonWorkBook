"""
выводит все изображения, имеющиеся в каталоге, в виде миниатюр на кнопках,
щелчок на которых приводит к выводу полноразмерного изображения; требует
наличия пакета PIL для отображения JPEG-файлов и создания миниатюр; что сделать:
добавить прокрутку, если в окне выводится слишком много миниатюр!
"""

import os
import sys
import math
from tkinter import *
from PIL import Image
from PIL.ImageTk import PhotoImage


def make_thumbs(img_dir, size=(100, 100), sub_dir='thumbs'):
    """
    создает миниатюры для всех изображений в каталоге; для каждого изображения
    создается и сохраняется новая миниатюра или загружается существующая;
    при необходимости создает каталог thumb;
    возвращает список кортежей (имя_файла_изображения, объект_миниатюры);
    для получения списка файлов миниатюр вызывающая программа может также
    воспользоваться функцией listdir в каталоге thumb; для неподдерживаемых
    типов файлов может возбуждать исключение IOError, или другое;
    ВНИМАНИЕ: можно было бы проверять время создания файлов;
    """
    thumb_dir = os.path.join(img_dir, sub_dir)
    if not os.path.exists(thumb_dir):
        os.mkdir(thumb_dir)

    thumbs = []
    for img_file in os.listdir(img_dir):
        thumb_path = os.path.join(thumb_dir, img_file)
        if os.path.exists(thumb_path):
            thumb_obj = Image.open(thumb_path)
            thumbs.append((img_file, thumb_obj))
        else:
            print('Making: {}'.format(thumb_path))
            img_path = os.path.join(img_dir, img_file)
            try:
                img_obj = Image.open(img_path)
                img_obj.thumbnail(size, Image.ANTIALIAS)
                img_obj.save(thumb_path)
                thumbs.append((img_file, img_obj))
            except Exception:
                print("Skipping: {}".format(img_path))
    return thumbs


class ViewOne(Toplevel):
    """
    открывает одно изображение в новом окне; ссылку на объект PhotoImage
    требуется сохранить: изображение будет утрачено при утилизации объекта;
    """
    def __init__(self, img_dir, img_file):
        Toplevel.__init__(self)
        self.title(img_file)
        img_path = os.path.join(img_dir, img_file)
        img_obj = PhotoImage(file=img_path)
        Label(self, image=img_obj).pack()
        print("[<{0}> <{1}x{2}>]".format(img_path, img_obj.width, img_obj.height()))
        self.saved_photo = img_obj


def viewer(img_dir, kind, cols=None):
    """
    создает окно с миниатюрами для каталога с изображениями: по одной кнопке с
    миниатюрой для каждого изображения;
    используйте параметр kind=Tk, чтобы вывести миниатюры в главном окне, или
    Frame (чтобы прикрепить к фрейму); значение imgfile изменяется в каждой
    итерации цикла: ссылка на значение должна сохраняться по умолчанию;
    объекты PhotoImage должны сохраняться: иначе при утилизации изображения
    будут уничтожены;
    компонует в ряды фреймов (в противоположность сеткам, фиксированным
    размерам, холстам);
    """
    win = kind()
    win.title('Viewer: {}'.format(img_dir))
    quit = Button(win, text="Quit", command=win.quit, bg="beige")
    quit.pack(fill=X, side=BOTTOM)      # добавить первой, чтобы урезалась последней
    thumbs = make_thumbs(img_dir)
    if not cols:
        cols = int(math.ceil(math.sqrt(len(thumbs))))       # фиксированное или N x N

    save_photos = []
    while thumbs:
        row_thumbs, thumbs = thumbs[:cols], thumbs[cols:]
        row = Frame(win)
        row.pack(fill=BOTH)
        for (img_file, img_obj) in row_thumbs:
            size = max(img_obj.size)        # ширина, высота
            photo = PhotoImage(img_obj)
            link = Button(row, image=photo)
            handler = lambda save_file=img_file: ViewOne(img_dir, save_file)
            link.config(command=handler, width=size, height=size)
            link.pack(side=LEFT, expand=YES)
            save_photos.append(photo)
    return win, save_photos


if __name__ == '__main__':
    img_dir = sys.argv[1] if len(sys.argv) > 1 else 'images'
    main, save = viewer(img_dir, kind=Tk)
    main.mainloop()
