import _thread as thread
import time


def counter(myId, count):                   # эта функция выполняется в потоках
    for i in range(count):
        time.sleep(1)                       # имитировать работу
        mutex.acquire()
        print("[%s] => %s" % (myId, i))     # теперь работа функции print
        mutex.release()                     # не будет прерываться


mutex = thread.allocate_lock()                  # создать объект блокировки
for i in range(5):                              # породить 5 потоков выполнения
    thread.start_new_thread(counter, (i, 5))    # каждый поток выполняет 5 циклов


time.sleep(6)                       # задержать выход из программы
print("Main thread exiting.")
