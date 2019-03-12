# Взаимодейтсвие потоков-потребителей и потоков-производителей, посредством очереди
import _thread as thread, queue, time
safe_print = thread.allocate_lock()     # Предотвратим перемешивание вывода
data_queue = queue.Queue()              # Общая очередь, не ограничена по размеру


num_consumers = 2  # Количество потоков-потребиетелей
num_producers = 4  # Количество потоков-производителей
num_messages = 4  # Количество сообщений, помещаемых производителем


def producer(id_num):
    for msg_num in range(num_messages):
        time.sleep(id_num)
        data_queue.put("[producer id={0}, count={1}]".format(id_num, msg_num))


def consumer(id_num):
    while True:
        time.sleep(0.1)
        try:
            data = data_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            with safe_print:
                print("consumer", id_num, "got=>", data)


if __name__ == '__main__':
    for i in range(num_consumers):
        thread.start_new_thread(consumer, (i,))
    for i in range(num_producers):
        thread.start_new_thread(producer, (i,))
    time.sleep(((num_producers-1) * num_messages) + 1)
    print("Main thread exiting")
