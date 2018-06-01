"""
stack.py: Модуль, реализущий структуру стека, при помощи класса Stack.
Методы класса: 1) __init__: инициализирует стек при содании(пустым списком)
               2) is_empty: проверка стека на пустоту(вернет True, если стек пуст)
               3) print_stack: вызывает приватный метод вывода стека, если он не пуст
               4) __printer: приватный метод, реализует вывод стека на экран в удобочитаемом виде
               5) push: помещает переданое ему значение value в вершину стека
               6) pop: удаляет вершину стека и возвращает ее значение
               7) peek: отображает значение вершины стека, ничего не удаляет
"""

class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return self.stack == []

    def print_stack(self):
        self.__printer() if not self.is_empty() else print("Stack is empty!")

    def __printer(self):
        sepline = "+--------+"
        output = ""
        for value in reversed(self.stack): output += "|{0:^8}|\n".format(value)
        print("\n{0}\n| Stack: |\n{0}\n{1}{0}".format(sepline, output))

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.is_empty():
            print("\n<IndexError: pop from empty stack!>\n")
        else:
            self.stack.pop()

    def peek(self):
        if self.is_empty():
            print("\n<IndexError: peek from empty stack!>\n")
        else:
            return self.stack[-1]

    def len_stack(self):
        return len(self.stack)


if __name__ == "__main__":
    stack = Stack()
    for x in range(5):
        stack.push(x)
    stack.peek()
    stack.print_stack()
    stack.pop()
    stack.print_stack()
    print(stack.len_stack())