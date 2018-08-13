"""то же самое, но скрывает и отображает окно целиком"""

from tkinter import *
import alarm


class Alarm(alarm.Alarm):
    def repeater(self):                             # каждые N миллисекунд
        self.bell()                                 # подать сигнал
        if self.master.state() == "normal":         # окно отображается?
            self.master.withdraw()                  # скрыть окно, без ярлыка
        else:
            self.master.deiconify()                 # иначе перерисовать окно
            self.master.lift()                      # и поднять над остальными
        self.after(self.msecs, self.repeater)       # переустановить обработчик


if __name__ == '__main__':
    Alarm().mainloop()
