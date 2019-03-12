from tkinter import *


class HelloButton(Button):
    def __init__(self, parent=None, **config):      # регистрирует метод callback
        Button.__init__(self, parent, **config)     # и добавляет себя в интерфейс
        self.pack()                                 # можно использовать старый
        self.configure(command=self.callback)       # стиль аргумента config

    def callback(self):                 # действие по умолчанию при нажатии
        print("Good bye world!")        # переопределить в подклассах
        self.quit()


if __name__ == '__main__':
    HelloButton(text="Subclass hello").mainloop()
