"""
реализует возможность рисования эластичных фигур на холсте при перемещении
указателя мыши с нажатой правой кнопкой; версии этого сценария, дополненные
тегами и анимацией, в файлах canvasDraw_tags*.py
"""

from tkinter import *

TRACE = True


class CanvasEventsDemo:
    def __init__(self, parent=None):
        canvas = Canvas(parent, width=300, height=300, bg="beige")
        canvas.pack()
        canvas.bind("<ButtonPress-1>", self.on_start)       # щелчок
        canvas.bind("<B1-Motion>", self.on_grow)            # и вытягивание
        canvas.bind("<Double-1>", self.on_clear)            # удалить все
        canvas.bind("<ButtonPress-3>", self.on_move)        # перемещать последнюю
        self.canvas = canvas
        self.drawn = None
        self.kinds = [canvas.create_oval, canvas.create_rectangle]

    def on_start(self, event):
        self.shape = self.kinds[0]
        self.kinds = self.kinds[1:] + self.kinds[:1]    # начало вытягивания
        self.start = event
        self.drawn = None

    def on_grow(self, event):                           # удалить и перерисовать
        canvas = event.widget
        if self.drawn:
            canvas.delete(self.drawn)
        obj_id = self.shape(self.start.x, self.start.y, event.x, event.y)
        if TRACE: print(obj_id)
        self.drawn = obj_id

    @staticmethod
    def on_clear(event):
        event.widget.delete("all")                      # использовать тег all

    def on_move(self, event):
        if self.drawn:                                  # передвинуть в позицию
            if TRACE: print(self.drawn)                 # щелчка
            canvas = event.widget
            dx, dy = event.x - self.start.x, event.y - self.start.y
            canvas.move(self.drawn, dx, dy)
            self.start = event


if __name__ == "__main__":
    root = Tk()
    CanvasEventsDemo(root)
    root.mainloop()
