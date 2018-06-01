import sys
from tkinter import Button, mainloop
from functools import reduce


def mysum(L):
    first, *rest = L
    return first if not rest else first + mysum(rest)   # Рекурсивный обход последовательности

L = [x for x in range(1, 6)]
print("\nL = {}\nmysum(L): {}".format(L, mysum(L)))
print("mysum(list('spam')): {}".format(mysum(list('spam'))))


def echo(massage):      # Имени echo присаивается объект функции
    print(massage)

echo("\nDirect call")    # Вызов объекта функции по оригинальному имени
x = echo                 # Теперь на эту функцию ссылается  еще и имя x
x("Indirect call!")      # Вызов объекта по дргому имени, добавлением пары скобок()

def indirect(func, arg):
    func(arg)

indirect(echo, "Argument call!")    # Передача функции в функию

schedule = [(echo, "Spam"), (echo, "Ham")]
for (func, arg) in schedule:
    func(arg)       # Вызов функции, сохраненной в контейрнере



f = lambda x, y, z: x + y + z       # Имени f присваивается объект функции, созданный lambda-выржением
print("\nf = lambda x, y, z: x + y + z\nf(1, 2, 3): {}".format(f(1, 2, 3)))

x = (lambda a="fee", b="fie", c="foe": a + b + c)       # lambda-выражение поодерж. параметры по умолчанию
print('\nx = lambda a="fee", b="fie", c="foe": x + y + z\nx("wee"): {}\n'.format(x("wee")))


L = [lambda x: x ** 2,  # Встроеные определения
     lambda x: x ** 3,
     lambda x: x ** 4]  # Список из трех функций

for f in L:
    print(f(2), end=' ')    # Выведет 4, 8, 16
print()

print(L[0](3), '\n')      # Выведет 3 ** 2  ->  9


lower = (lambda x, y: x if x < y else y)    # Логика выбора внутри lambda-выражения
print(lower(1, 44))
print(lower('ff', 'cc'), '\n')


showall = lambda x: list(map(sys.stdout.write, x))
showall(['spam\n', 'eggs\n', 'ham\n'])
print()                        # Использование генераторов и map для выполнения логики циклов внутри lambda-выражения

showall = lambda x: [sys.stdout.write(line) for line in x]
showall(['spam\n', 'eggs\n', 'ham\n'])


def action(x):
    return lambda y: x + y      # Создать и вернуть объект-функцию, запомнить x

x = 3
y = 99
act = action(y)
print("\n{} + {} = {}".format(y, x, act(x)))  # Вывзвать функцию, созданную функцией action

action = lambda x: lambda y: x + y      # Вернуть объект-функцию, при помощи объекта-функции!
act = action(y)
print("{} + {} = {}".format(y, x, act(x)))  # Вывзвать функцию, созданную lambda-инструкцией


x = Button(text="Press me",
    	   command=lambda: sys.stdout.write("Spam\n"))
x.pack()
mainloop()


L = [x for x in range(-5, 6)]
res = list(filter(lambda x: x > 0, L))
print("\nL = {}\nfilter(lambda x: x > 0, L): {}".format(L, res))


print("sum of res = {}".format(reduce(lambda x, y: x + y, res)))