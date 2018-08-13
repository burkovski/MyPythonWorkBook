"""мигает и издает сигнал каждую секунду, используя цикл с методом after()"""

from tkinter import *


class Alarm(Frame):
    def __init__(self, msecs=1000):         # по умолчанию = 1 секунда
        Frame.__init__(self)
        self.msecs = msecs
        self.pack()
        stopper = Button(self, text="Stop the beeps!", command=self.quit)
        stopper.pack()
        stopper.config(bg="navy", fg="white", bd=8)
        self.stopper = stopper
        self.repeater()

    def repeater(self):                             # каждые N миллисекунд
        self.bell()                                 # подать сигнал
        self.stopper.flash()                        # мигнуть кнопкой
        self.after(self.msecs, self.repeater)       # запланировать следующий вызов1


if __name__ == "__main__":
    Alarm().mainloop()
