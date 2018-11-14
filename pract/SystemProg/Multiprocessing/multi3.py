"""
Реализует взаимодействие с помощью объектов разделяемой памяти из пакета.
В Windows передаваемые объекты используются совместно, а глобальные объекты
- нет. Последняя проверка здесь отражает типичный случай использования:
распределение заданий между процессами.
"""

import os
from multiprocessing import Process, Value, Array

procs = 3       # глобальные переменные, отдельные для каждого процесса, не являются совместно используемыми
count = 0


def showdata(label, val, arr):
    """
    выводит значения данных в этом процессе
    """
    msg = "{0:<12}: pid:{1:4}, global:{2}, value:{3}, array:{4}"
    print(msg.format(label, os.getpid(), count, val.value, list(arr)))


def updater(val, arr):
    """
    обменивается данными через разделяемую память
    """
    global count
    count += 1          # глобальный счетчик  недоступен другим процессам
    val.value += 1      # а передаваемый в объекте - доступен
    for i in range(procs):
        arr[i] += 1


if __name__ == '__main__':
    scalar = Value('i', 0)          # разделяемая память: предусматривает синхронизацию процессов/потоков
    vector = Array('d', procs)      # коды типов из ctypes: int, double

    # вывести начальные значения в родительском процессе
    showdata("parent start", scalar, vector)

    # породить дочерний процесс, передать данные в разделяемой памяти
    p = Process(target=showdata, args=("child", scalar, vector))
    p.start()
    p.join()

    # изменить значения в родителе и передать через разделяемую память,
    # ждать завершения каждого потомка
    # все потомки видят изменения, выполненные в родительском процессе и
    # переданные в виде аргументов (но не в глобальной памяти)
    print("\nloop#1 [updates in parent, serial children]...")
    for i in range(procs):
        count += 1
        scalar.value += 1
        vector[i] += 1
        p = Process(target=showdata, args=("process#{}".format(i+1),
                                           scalar, vector))
        p.start()
        p.join()

    # то же самое, но потомки запускаются параллельно
    # все они видят результат последней итерации, потому что они хранятся
    # в совместно используемых объектах
    print("\nloop#2 [updates in parent, parallel children]...")
    ps = []
    for i in range(procs):
        count += 1
        scalar.value += 1
        vector[i] += 1
        p = Process(target=showdata, args=("process#{}".format(i + 1),
                                           scalar, vector))
        p.start()
        ps.append(p)
    for p in ps:
        p.join()

    # объекты в разделяемой памяти изменяются потомками,
    # ждать завершения каждого из них
    print("\nloop#3 [updates in serial children]...")
    for i in range(procs):
        p = Process(target=updater, args=(scalar, vector))
        p.start()
        p.join()
    showdata("parent temp", scalar, vector)

    # то же самое, но потомки запускаются параллельно
    ps = []
    print("\nloop#4 [updates in parallel children]...")
    for i in range(procs):
        p = Process(target=updater, args=(scalar, vector))
        p.start()
        ps.append(p)
    for p in ps:
        p.join()
    showdata("parent end", scalar, vector)
