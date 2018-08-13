"""
перемещение с применением тегов и функции time.sleep (без помощи метода widget.
after или потоков выполнения); функция time.sleep не блокирует цикл событий
графического интерфейса на время паузы, но интерфейс не обновляется до выхода из
обработчика или вызова метода widget.update; текущему вызову обработчика onMove
уделяется исключительное внимание, пока он не вернет управление: если в процессе
перемещения нажать клавишу ‘R’ или ‘O’;
"""

from tkinter import *
import canvasDraw
import time


class CanvasEventsDemo(canvasDraw.CanvasEventsDemo):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas.create_text(150, 10, text="Press <O> and <R> to move shapes")
        self.canvas.master.bind("<KeyPress-o>", self.on_move_ovals)
        self.canvas.master.bind("<KeyPress-r>", self.on_move_rectangles)
        self.kinds = (self.create_oval_tagged, self.create_rectangle_tagged)

    def create_oval_tagged(self, x1, y1, x2, y2):
        obj_id = self.canvas.create_oval(x1, y1, x2, y2)
        self.canvas.itemconfig(obj_id, tag="ovals", fill="blue")
        return obj_id

    def create_rectangle_tagged(self, x1, y1, x2, y2):
        obj_id = self.canvas.create_rectangle(x1, y1, x2, y2)
        self.canvas.itemconfig(obj_id, tag="rectangles", fill="red")
        return obj_id

    def on_move_ovals(self, event):
        print("moving ovals")
        self.move_in_squares(tag="ovals")

    def on_move_rectangles(self, event):
        print("moving rectangles")
        self.move_in_squares(tag="rectangles")

    def move_in_squares(self, tag):
        for _ in range(5):
            for (dx, dy) in [(+20, 0), (0, +20), (-20, 0), (0, -20)]:
                self.canvas.move(tag, dx, dy)
                self.canvas.update()
                time.sleep(0.25)


if __name__ == "__main__":
    root = Tk()
    CanvasEventsDemo(root)
    root.mainloop()
