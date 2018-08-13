"""
аналогично, но с применением метода widget.after() вместо циклов time.sleep;
поскольку это планируемые события, появляется возможность перемещать овалы
и прямоугольники _одновременно_ и отпадает необходимость вызывать метод update
для обновления графического интерфейса; движение станет беспорядочным, если еще
раз нажать ‘o’ или ‘r’ в процессе воспроизведения анимации: одновременно начнут
выполняться несколько операций перемещения;
"""

from tkinter import *
import canvasDraw_tags


class CanvasEventsDemo(canvasDraw_tags.CanvasEventsDemo):
    def moveEm(self, tag, more_moves):
        (dx, dy), *more_moves = more_moves
        self.canvas.move(tag, dx, dy)
        if more_moves:
            self.canvas.after(250, self.moveEm, tag, more_moves)

    def move_in_squares(self, tag):
        all_moves = [(+20, 0), (0, +20), (-20, 0), (0, -20)] * 5
        self.moveEm(tag, all_moves)


if __name__ == '__main__':
    CanvasEventsDemo()
    mainloop()
