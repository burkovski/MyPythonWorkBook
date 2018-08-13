"""
простой компонент холста с вертикальной прокруткой
"""

from tkinter import *


class ScrolledCanvas(Frame):
    def __init__(self, parent=None, color="brown", **options):
        super(ScrolledCanvas, self).__init__(parent, **options)
        self.pack(expand=YES, fill=BOTH)                            # сделать растягиваемым
        canvas = Canvas(self, bg=color, relief=SUNKEN)
        canvas.config(width=300, height=200)                        # размер видимой области
        canvas.config(scrollregion=(0, 0, 300, 1000))               # углы холста
        canvas.config(highlightthickness=0)                         # без рамки

        s_bar = Scrollbar(self)
        s_bar.config(command=canvas.yview)              # связать s_bar и canvas
        canvas.config(yscrollcommand=s_bar.set)         # сдвиг одного = сдвиг другого
        s_bar.pack(side=RIGHT, fill=Y)                  # первым добавлен – посл. обрезан
        canvas.pack(side=LEFT, expand=YES, fill=BOTH)   # canvas обрезается первым
        self.canvas = canvas

        self.fill_content()
        self.canvas.bind("<Double-1>", self.on_doubleclick)    # установить обр. события

    def fill_content(self):         # переопределить при наследовании
        for i in range(10):
            self.canvas.create_text(
                150, 50+(i*100),
                text="Spam #{}".format(i),
                fill="beige"
            )

    def on_doubleclick(self, event):        # переопределить при наследовании
        print(event.x, event.y)
        print(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))


if __name__ == "__main__":
    ScrolledCanvas().mainloop()

