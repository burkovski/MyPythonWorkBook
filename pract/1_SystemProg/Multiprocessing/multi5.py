"""
Использует пакет multiprocessing для запуска независимых программ,
с помощью os.fork или других функций
"""

import os
from multiprocessing import Process


def run_program(arg):
    os.execlp("python", "python", "child.py", str(arg))


if __name__ == '__main__':
    for i in range(5):
        p = Process(target=run_program, args=(i, ))
        p.start()
        p.join()
    print("Parent exit...")