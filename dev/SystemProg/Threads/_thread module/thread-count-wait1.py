import _thread as thread
stdoutmutex = thread.allocate_lock()
exitmutexes = [thread.allocate_lock() for i in range(5)]


def counter(myId, count):
    for i in range(count):
        stdoutmutex.acquire()
        print("[%s] => %s" % (myId, i))
        stdoutmutex.release()
    exitmutexes[myId].acquire()         # Сигнал главному потоку


for i in range(5):
    thread.start_new_thread(counter, (i, 5))

for mutex in exitmutexes:
    while not mutex.locked(): pass
print("Main thread exiting")
