import sys


def f(a):       # Имени a присваивается переданый объект
    a = 99      # Изменяется только локальная переменная

b = 88
f(b)        # Первоначально имена а и b ссылаются на одно и то же число 88
print("B =", b)    # Переменная b не изменилась


def changer(a, b):      # В аргументах передаются ссылки на объекты
    a = 2               # Изменяется только значение локального имени
    b[0] = 'spam'       # Изменяется непосредстевнно разделяемый объект

x = 1
l = [1, 2]                                  # Вызывающая программа
print("\nBefore changer() call:", x, l)
changer(x, l)                               # Передаются изменяемый и неизмменяемый объекты
print("After changer() call:", x, l)        # Переменная х не изменилась, l - изменился


def multiple(x, y):
    x = 2           # Изменяется локальное имя
    y = [3, 4]
    return x, y     # Новые значнения возвращаются в виде кортежа

x = 1
l = [1, 2]
print("\nBefore multiple() call:", x, l)
x, l = multiple(x, l)                       # Результаты возвращаются именам в вызввающей программе
print("After multiple() call:", x, l, '\n')



def f(a, b, c):
    print("f(a, b, c):", a, b, c)

f(1, 2, 3)      # Позиционные аргументы: значению a присваетвается 1,  b - 2, c - 3     (соотв. по позициям)
f(c=3, a=1, b=2)    # Именованые аргументы - явно определяют соотвествие между значениями и именами   (соотв. по именам)
f(1, c=3, b=2)      # Комбинированая форма. Первыми сопост. позиционные аргументы, далее - именованые
print()


def f(a, b=2, c=3):         # Один аргумент - обязательный, два других имеют значения по умолчанию
    print("f(a, b=2, c=3):", a, b, c)

f(1)            # Значение передается агрументу a
f(a=1)
f(1, 4)         # Переопределение аргументов по умолчанию
f(1, c=5)
print()


def f(*args):                      # Сбор позиционных аргументов в кортеж
    print("f(*args):", args)

f()
f(1)
f(1, 2, 3, 4)
print()


def f(**kwargs):                    # Сбор именованых аргументов в словарь
    print("f(**kwargs):", kwargs)

f()
f(a=1, b=2, c=3)
print()


def f(a, *args, **kwargs):       # Комбинированая форма
    print("f(a, *args, **kwargs): {}, {}, {}".format(a, args, kwargs))

f(1, 2, 3, x=4, y=5)
print()


def func(a, b, c, d):       # Ожидает 4 аргумента
    print("func(a, b, c, d):", a, b, c, d)

args = (1, 2)
args += (3, 4)
func(*args)                                 # Распаковывает кортеж из 4 элементов (позиционные аргументы)
args = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
func(**args)                                # Распаковывает словарь из 4 элементов (именованые аргументы)


def tracer(func, *args, **kwargs):          # Принимает произвольные аругменты
    print("calling:", func.__name__)
    return func(*args, **kwargs)            # Передает все полученные аргументы

def func(a, b, c, d):
    return a + b + c + d

print(tracer(func, 1, 2, c=3, d=4))


# Функции нахождения минимума:
def min1(*args):
    res = args[0]
    for arg in args[1:]:
        if arg < res:
            res = arg
    return res


def min2(first, *rest):
    for arg in rest:
        if arg < first:
            first = arg
    return first


def min3(*args):
    tmp = list(args)
    tmp.sort()
    return tmp[0]

T = (3, 4, 1, -1, 0, 63, -2)
print("\nT =", T)
print("min1():", min1(*T))
print("min2():", min2(*T))
print("min3():", min3(*T))


def minmax(test, first, *rest):         # Универсальная функция поиска миммума/максимума
    for arg in rest:
        if test(arg, first):
            first = arg
    return first

def lessthan(x, y):
    return x < y
def greaterthan(x, y):
    return x > y

print("minmax(min):", minmax(lessthan, *T))
print("minmax(max):", minmax(greaterthan, *T))


# Функции множеств
def intersect(first, *rest):
    res = []
    for x in first:                 # Сканировать первую последовательность
        for other in rest:          # Во всех остальных аргументах
            if x in other:          # Общиий элемент?
                res.append(x)       # Да: добавить элемент в результирующий список
            break
    return res


def union(*args):
    res = []
    for seq in args:            # Для всех аргументов
        for x in seq:           # Для всех элементов
            if not x in res:    # Если эелемент - новый:
                res.append(x)   # Добавить в конец
    return res

s1, s2, s3 = "SPAM", "SCAM", "SLAM"
print("\ns1 = {}\ns2 = {}\ns3 = {}".format(s1, s2, s3))
print("intersect(s1, s2, s3): {}".format(intersect(s1, s2, s3)))
print("union(s1, s2, s3): {}".format(union(s1, s2, s3)))



# Аналог функции print()
def myprint1(*args, **kwargs):
    sep = kwargs.pop('sep', ' ')        # Именованые аргументы
    end = kwargs.pop('end', '\n')       # Со значением по умолчанию
    file = kwargs.pop('file', sys.stdout)
    if kwargs:
        raise TypeError("extra keywords %s" % kwargs)
    output = ""
    first = True
    for arg in args:
        output += ('' if first else sep) + str(arg)
        first = False
    file.write(output + end)

myprint1("\nMy print func!:", 1, 2, 3)
myprint1("My print func!:", 1, 2, 3, sep='...')
myprint1("My print func!:", 1, 2, 3, sep=' |&&| ', end=' !..')


def myprint2(*args, sep=' ', end='\n', file=sys.stdout):    # Именованые аргументы
    output = ""
    first = True
    for arg in args:
        output += ('' if first else sep) + str(arg)
        first = False
    file.write(output + end)

myprint2("\n\nMy print func!:", 1, 2, 3)
myprint2("My print func!:", 1, 2, 3, sep='...')
myprint2("My print func!:", 1, 2, 3, sep=' |&&| ', end=' !..')
