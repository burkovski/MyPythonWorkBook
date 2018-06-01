import threading


class MyThread(threading.Thread):          # Подкласс класса Thread
    def __init__(self, my_id, count, mutex):
        self.my_id = my_id
        self.count = count                 # Информация для каждого потока
        self.mutex = mutex                 # Совместно используемые объекты,
        threading.Thread.__init__(self)    # вместо глобальных переменных

    def run(self):
        for i in range(self.count):        # run реализует логику потока
            with self.mutex:               # синхронизовать доступ к stdout
                print("[{0}] => {1}".format(self.my_id, i+1))


stdout_mutex = threading.Lock()
threads = []
for i in range(2):
    thread = MyThread(i+1, 2, stdout_mutex)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
print("Main thread exiting")