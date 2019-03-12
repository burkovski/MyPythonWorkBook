"""
тест очереди обработчиков, но для реализации операций
используются связанные методы
"""

import time
from threadtools import thread_checker, start_thread
from tkinter.scrolledtext import ScrolledText


class MyGUI:
    def __init__(self, reps=3):
        self.reps = reps
        self.text = ScrolledText()          # сохранить виджет в атрибуте
        self.text.pack()
        thread_checker(self.text)           # запустить цикл проверки потоков
        self.text.bind("<Button-1>", lambda event: list(map(self.on_event, range(6))))
        self.text.bind("<Button-3>", lambda event: self.text.quit())

    def on_event(self, i):          # метод, запускающий поток
        my_name = "[Thread-{}]".format(i)
        start_thread(
            action=self.thread_action,
            args=(i, ),
            context=(my_name, ),
            on_exit=self.thread_exit,
            on_fail=self.thread_fail,
            on_progress=self.thread_progress)

    # основная операция, выполняемая потоком
    def thread_action(self, id, progress):      # то, что делает поток
        for i in range(self.reps):              # доступ к данным в объекте
            time.sleep(1)
            if progress: progress(i)            # обработчик progress: в очередь
        if id % 2 == 0: raise Exception         # ошибочный номер: неудача

    # обработчики: передаются главному потоку через очередь
    def thread_exit(self, my_name):
        self.text.insert("end", "{}\texit\n".format(my_name))
        self.text.see("end")

    def thread_fail(self, exc_info, my_name):       # имеет доступ к данным объекта
        self.text.insert("end", "{}\tfail\t{}\n".format(my_name, exc_info[0]))
        self.text.see("end")

    def thread_progress(self, count, my_name):
        self.text.insert("end", "{}\tprog\t{}\n".format(my_name, count))
        self.text.see("end")
        self.text.update()


if __name__ == "__main__":
    MyGUI().text.mainloop()
