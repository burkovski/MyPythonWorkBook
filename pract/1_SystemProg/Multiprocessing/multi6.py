"""
Плюс многое другое: пулы процессов, менеджеры, блокировки,
условные переменные,...
"""

import os
from multiprocessing import Pool, Process


def powers(x):
    # print(os.getpid())
    return 2 ** x


if __name__ == '__main__':
    reps = 100
    workers = Pool(processes=5)

    results = workers.map(powers, [2]*reps)
    print(results[:16])
    print(results[-2:])

    results = workers.map(powers, range(reps))
    print(results[:16])
    print(results[-2:])
