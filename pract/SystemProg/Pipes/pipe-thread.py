# анонимные каналы и потоки выполнения вместо процессов;
import os
import time
import threading


def child(pipeout):
    zzz = 0
    while True:
        time.sleep(zzz)                             # заставить родителя подождать
        msg = "Spam {0:03}".format(zzz).encode()    # каналы - двоичные данные
        os.write(pipeout, msg)                      # отправить данные родителю через канал
        zzz = (zzz+1) % 5


def parent(pipein):
    while True:
        line = os.read(pipein, 32)                  # остановиться до получения данных
        print("Parent {0} got [{1}] at {2:.5f}".format(os.getpid(), line, time.time()))


pipein, pipeout = os.pipe()
threading.Thread(target=child, args=(pipeout, )).start()
parent(pipein)