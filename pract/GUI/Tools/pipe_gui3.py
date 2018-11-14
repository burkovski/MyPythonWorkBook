"""
читает данные из канала в отдельном потоке выполнения и помещает их в очередь,
которая проверяется в цикле обработки событий от таймера; позволяет сценарию
отображать вывод программы, не вызывая блокирование графического интерфейса
между операциями вывода; со стороны дочерних программ не требуется выполнять
подключение или выталкивать буферы, но данное решение сложнее, чем подход на
основе сокетов
"""

import _thread as thread
import queue
import os
from tkinter import Tk
from pract.GUI.Tools.guiStreams import GuiOutput

stdout_queue = queue.Queue()         # бесконечной длины


def producer(input):
    while True:
        line = input.readline()     # блокирование не страшно: дочерний поток
        stdout_queue.put(line)      # пустая строка - конец файла
        if not line:
            break


def consumer(output, root, term="<end>"):
    try:
        line = stdout_queue.get(block=False)        # главный поток: проверять очередь
    except queue.Empty:                             # 4 раза в сек, это нормально,
        pass                                        # если очередь пуста
    else:
        if not line:                    # остановить цикл по достижении конца файла
            output.write(term)          # иначе отобразить следующую строку
            return
        output.write(line)
    root.after(250, lambda: consumer(output, root, term))


def redirected_gui_shell_cmd(command, root):
    input = os.popen(command, 'r')          # запустить программу командной строки
    output = GuiOutput(root)
    thread.start_new_thread(producer, (input, ))        # запустить поток чтения
    consumer(output, root)


if __name__ == "__main__":
    win = Tk()
    redirected_gui_shell_cmd("python -u pipe-nongui.py", win)
    win.mainloop()
