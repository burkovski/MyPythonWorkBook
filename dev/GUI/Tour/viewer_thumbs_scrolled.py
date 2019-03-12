"""
расширенная версия сценария просмотра изображений: отображает миниатюры на
кнопках фиксированного размера, чтобы обеспечить равномерное их размещение,
и добавляет возможность прокрутки при просмотре больших коллекций изображений,
отображая миниатюры в виджете Canvas с полосами прокрутки; требует наличия
библиотеки PIL для отображения изображений в таких форматах, как JPEG, и повторно
использует инструменты создания миниатюр и просмотра единственного изображения из
сценария viewer_thumbs.py; предостережение/что сделать: можно также реализовать
возможность прокрутки при отображении единственного изображения, если его размеры
оказываются больше размеров экрана, которое сейчас обрезается в Windows;
"""

import math
from tkinter import *
from PIL.ImageTk import PhotoImage
from viewer_thumbs import make_thumbs, ViewOne


def viewer(img_dir, kind=Toplevel, num_cols=None, width=300, height=300):
    """
    использует кнопки фиксированного размера и холст с возможностью прокрутки;
    определяет размер области прокрутки (всего холста) и располагает
    миниатюры по абсолютным координатам x,y холста; предупреждение:
    предполагается, что все миниатюры имеют одинаковые размеры
    """
    win = kind()
    win.title("Simple viewer: {}".format(img_dir))
    quit = Button(win, text="Quit", command=win.quit, bg="beige")
    quit.pack(side=BOTTOM, fill=X)

    canvas = Canvas(win, borderwidth=0)
    h_bar = Scrollbar(win, orient="horizontal")
    v_bar = Scrollbar(win)

    v_bar.pack(side=RIGHT, fill=Y)          # прикрепить холст после полос прокрутки
    h_bar.pack(side=BOTTOM, fill=X)         # чтобы он обрезался первым
    canvas.pack(side=TOP, expand=YES, fill=BOTH)

    v_bar.config(command=canvas.yview)          # обработчики событий
    h_bar.config(command=canvas.xview)          # перемещения полос прокрутки
    canvas.config(yscrollcommand=v_bar.set)     # обработчики событий
    canvas.config(xscrollcommand=h_bar.set)     # прокрутки холста
    canvas.config(width=width, height=height)   # начальные размеры видимой области,
                                                # изменяемой при изменении размеров окна

    thumbs = make_thumbs(img_dir=img_dir)       # [(img_file, img_obj)]
    num_thumbs = len(thumbs)
    if not num_cols:
        num_cols = int(math.ceil(math.sqrt(num_thumbs)))        # фиксиров. или N x N
    num_rows = int(math.ceil(num_thumbs / num_cols))

    link_size = max(thumbs[0][1].size)
    full_size = (
        0, 0,                                           # верхний левый угол X,Y
        link_size * num_cols, link_size * num_rows      # нижний правый угол X,Y
    )
    canvas.config(scrollregion=full_size)               # размер области прокрутки

    row_pos = 0
    save_photos = []
    while thumbs:
        thumbs_row, thumbs = thumbs[:num_cols], thumbs[num_cols:]
        col_pos = 0
        for (img_file, img_obj) in thumbs_row:
            photo = PhotoImage(img_obj)
            link = Button(canvas, image=photo)
            handler = lambda save_file=img_file: ViewOne(img_dir, save_file)
            link.config(command=handler, width=link_size, height=link_size)
            link.pack(side=LEFT, expand=YES)
            canvas.create_window(
                col_pos, row_pos,
                anchor=NW,
                window=link,
                width=link_size,
                height=link_size
            )
            col_pos += link_size
            save_photos.append(photo)
        row_pos += link_size
    return win, save_photos


if __name__ == "__main__":
    img_dir = "../../PIL/images" if len(sys.argv) < 2 else sys.argv[1]
    main, save = viewer(img_dir, kind=Tk)
    main.mainloop()
