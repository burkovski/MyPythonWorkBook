"""
графический интерфейс, отображающий данные,
производимые рабочими потоками (на основе классов)
"""

import threading
import queue
import time
from tkinter.scrolledtext import ScrolledText


class ThreadGui(ScrolledText):
    threads_per_click = 4

    def __init__(self, parent=None):
        ScrolledText.__init__(self, parent)
        self.pack()
        self.data_queue = queue.Queue()
        self.bind("<Button-1>", self.make_threads)
        self.bind("<Button-3>", lambda event: self.quit())
        self.consumer()

    def producer(self, id):
        for i in range(5):
            time.sleep(2)
            self.data_queue.put("[producer id={}, count={}]".format(id, i))

    def consumer(self):
        try:
            data = self.data_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            self.insert("end", "consumer got => {}\n".format(data))
            self.see("end")
        self.after(100, self.consumer)

    def make_threads(self, event):
        for i in range(self.threads_per_click):
            threading.Thread(target=self.producer, args=(i, )).start()


if __name__ == "__main__":
    root = ThreadGui()
    root.mainloop()
