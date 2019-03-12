import _thread as thread
import time


def counter(myId, count):           # Эта ф-ция выполняется в потоках
    for i in range(count):
        time.sleep(1)               # Имитировать работу
        print("[%s] => %s" % (myId, i))


for i in range(5):                              # Породить 5 потоков выполнения
    thread.start_new_thread(counter, (i, 5))    # Каждый поток выполняет 5 циклов


time.sleep(6)                       # Задержать выход из программы
print("Main thread exiting.")