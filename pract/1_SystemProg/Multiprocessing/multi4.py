"""
От класса Process можно породить подкласс, так же, как от класса threading.
Thread;
объект Queue действует подобно queue.Queue, но обеспечивает обмен данными между
процессами, а не между потоками выполнения
"""

import os
import queue
import time
from multiprocessing import Process, Queue  # общая очередь для процессов очередь - это канал + блокировки/семафоры


class Counter(Process):
    label = '  @'

    def __init__(self, start, queue):   # сохраняет данные для использования в методе run
        self.state = start
        self.post = queue
        Process.__init__(self)

    def run(self):      # вызывается в новом процессе методом start()
        for i in range(3):
            time.sleep(1)
            self.state += 1
            print(self.label, self.pid, self.state)     # self.pid - pid потомка
            self.post.put([self.pid, self.state])       # stdout совместно используется всеми
        print(self.label, self.pid, '-')


if __name__ == '__main__':
    print("start:", os.getpid())
    expected = 9

    post = Queue()
    p = Counter(0, post)        # запустить 3 процесса, использующих общую очередь
    q = Counter(100, post)      # потомки являются производителями
    r = Counter(1000, post)
    for process in (p, q, r):
        process.start()

    que = []
    while expected:         # родитель потребляет данные из очереди
        time.sleep(0.5)     # очень напоминает графический интерфейс,
        try:                # хотя в ГИ часто используются потоки
            data = post.get(block=True)
        except queue.Empty:
            print("no data...")
        else:
            print("posted:", data)
            expected -= 1
            que.append(data)

    res = []
    for process in (p, q, r):
        process.join()                  # дождаться завершения дочерних процессов
        res.append(process.exitcode)    # exitcode - код завершения потомка

    print("finish:", os.getpid(), res)
    print(que)
