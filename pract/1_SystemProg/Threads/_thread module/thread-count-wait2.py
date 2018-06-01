import _thread as thread
stdoutmutex = thread.allocate_lock()
exitmutexes = [False] * 5


def counter(myId, count):
    for i in range(count):
        stdoutmutex.acquire()
        print("[%s] => %s" % (myId, i))
        stdoutmutex.release()
    exitmutexes[myId] = True         # Сигнал главному потоку


for i in range(5):
    thread.start_new_thread(counter, (i, 5))

while False in exitmutexes: pass
print("Main thread exiting")
