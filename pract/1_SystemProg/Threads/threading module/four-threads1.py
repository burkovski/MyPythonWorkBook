import threading
import _thread


def action(i):
    print(i ** 32)


# Подкласс, хранящий собственную информацию о состоянии
class MyThread(threading.Thread):
    def __init__(self, i):
        self.i = i
        threading.Thread.__init__(self)

    def run(self):
        print(self.i ** 32)


MyThread(2).start()             # start вызовет run


# передача простой функции
thread = threading.Thread(target=(lambda: action(2)))       # run вызовет target
thread.start()


# то же самое, но без lambda-функции,
# сохраняющей информацию о состоянии в образуемом ею замыкании
threading.Thread(target=action, args=(2, )).start()     # вызываемый объект и его аргументы
