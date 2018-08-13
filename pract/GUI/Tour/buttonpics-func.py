from tkinter import *       # импортировать базовый набор виджетов,
from glob import glob       # чтобы получить список файлов по расширению
import random
import demoCheck            # прикрепить демонстрационный пример с флажками

dir_gifs = "../gifs/"       # каталог по умолчанию с GIF-файлами


def draw():
    name, photo = random.choice(images)
    lbl.config(text=name)
    pix.config(image=photo)


root = Tk()
lbl = Label(root, text="None", bg="blue", fg="red")
pix = Button(root, text="Press me", command=draw, bg="white")
lbl.pack(fill=BOTH)
pix.pack(pady=10)
demoCheck.Demo(root, relief=SUNKEN, bd=2).pack(fill=BOTH)
images = [(x, PhotoImage(file=x)) for x in glob(dir_gifs + "*.gif")]    # имеющиеся GIF-файлы загрузить и сохранить
print(images)
root.mainloop()


