class tracer1:                    # Трассировка вызова функции
    def __init__(self, func):       # На этапе декорировния @
        self.func = func            # Сохраняет оригинальную функцию func
        self.calls = 0
    def __call__(self, *args, **kwargs):  # При последующих вызовах: вызывает оригинальную функцию func
        self.calls += 1
        res = ", ".join([str(x) for x in args])
        if args and kwargs: res += ", "
        res += ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print("call #{0} to {1}({2}) => ".format(self.calls, self.func.__name__, res), end='')
        return self.func(*args, **kwargs)

@tracer1
def func(a, b, c):      # func = Tracer(func)
    print(a + b + c)
@tracer1
def spam(x, y):
    return x ** y

print('-' * 40)
func('a', 'b', 'c')     # func.__call__('a', 'b', 'c')
func(a=1, b=2, c=3)
print("func.calls = {}".format(func.calls))
print(spam(2, 4))
print(spam(4, y=2))
tmp = spam(2, 8)
print(tmp)
print("spam.calls = {}".format(spam.calls))
print('-' * 40)


calls = 0
def tracer2(func):
    def wrapper(*args, **kwargs):
        global calls    # Глобальная переменная, общая для всех декорируемых функций
        calls += 1
        res = ", ".join([str(x) for x in args])
        if args and kwargs: res += ", "
        res += ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print("call #{0} to {1}({2}) => ".format(calls, func.__name__, res), end='')
        return func(*args, **kwargs)
    return wrapper

@tracer2
def func(a, b, c):      # func = Tracer(func)
    print(a + b + c)
@tracer2
def spam(x, y):
    return x ** y

print('-' * 40)
func('a', 'b', 'c')     # wrapper('a', 'b', 'c')
func(a=1, b=2, c=3)
print("calls = {}".format(calls))
print(spam(2, 4))
print(spam(4, y=2))
tmp = spam(2, 8)
print(tmp)
print("calls = {}".format(calls))
print('-' * 40)


def tracer3(func):
    calls = 0
    def wrapper(*args, **kwargs):
        nonlocal calls    # Переменная в объеслющей области видимости, уникальная для каждой декуорируемой функции
        calls += 1
        res = ", ".join([str(x) for x in args])
        if args and kwargs: res += ", "
        res += ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print("call #{0} to {1}({2}) => ".format(calls, func.__name__, res), end='')
        return func(*args, **kwargs)
    return wrapper

@tracer3
def func(a, b, c):      # func = Tracer(func)
    print(a + b + c)
@tracer3
def spam(x, y):
    return x ** y

print('-' * 40)
func('a', 'b', 'c')     # wrapper('a', 'b', 'c')
func(a=1, b=2, c=3)
print(spam(2, 4))
print(spam(4, y=2))
tmp = spam(2, 8)
print(tmp)
print('-' * 40)


def tracer4(func):
    def wrapper(*args, **kwargs):
        wrapper.calls += 1      # Счеткчик хранится в атрибуте функции
        res = ", ".join([str(x) for x in args])
        if args and kwargs:
            res += ", "
        res += ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print("call #{0} to {1}({2}) => ".format(wrapper.calls, func.__name__, res), end='')
        return func(*args, **kwargs)
    wrapper.calls = 0   # Присоеденить атрибут к функции, у каждой декорируемой - свой
    return wrapper

@tracer4
def func(a, b, c):      # func = Tracer(func)
    print(a + b + c)
@tracer4
def spam(x, y):
    return x ** y

print('-' * 40)
func('a', 'b', 'c')     # wrapper('a', 'b', 'c')
func(a=1, b=2, c=3)
print("func.calls = {}".format(func.calls))
print(spam(2, 4))
print(spam(4, y=2))
tmp = spam(2, 8)
print(tmp)
print("spam.calls = {}".format(spam.calls))
print('-' * 40)



def tracer(func):       # Вместо класса с методом __call__, используется функция
    calls = 0           # иначе, "self" будет представлять экземпляр класса декоратора
    def onCall(*args, **kwargs):
        nonlocal calls
        calls += 1
        res = ", ".join([str(x) for x in args])
        if args and kwargs:
            res += ", "
        res += ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print("call #{0} to {1}({2}) => ".format(calls, func.__name__, res), end='')
        return func(*args, **kwargs)
    return onCall

@tracer             # Может применяться к функциям
def func(a, b, c):      # func = Tracer(func)
    print(a + b + c)
@tracer
def spam(x, y):
    return x ** y

print('-' * 40)
func('a', 'b', 'c')     # wrapper('a', 'b', 'c')
func(a=1, b=2, c=3)
print(spam(2, 4))
print(spam(4, y=2))
tmp = spam(2, 8)
print(tmp)
print("Methods...")

class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
    @tracer
    def lastName(self):
        return self.name.split()[-1]
    @tracer
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))

bob = Person("Bob Smith", 100000)
sue = Person("Sue Jones", 50000)
print(bob.name, sue.name)
sue.giveRaise(.10)
print()
print(bob.pay, sue.pay)
print(bob.lastName())
print(sue.lastName())
print('-' * 40)


class tracer:
    def __init__(self, func):   # На этапе декорирования
        # print("tracer init:", func)
        self.func = func
        self.calls = 0
    def __call__(self, *args, **kwargs):    # При обращении к обычным функциям
        # print("tracer call")
        self.calls += 1
        res = ", ".join([str(x) for x in args])
        if args and kwargs:
            res += ", "
        res += ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print("call #{0} to {1}({2}) => ".format(self.calls, self.func.__name__, res), end='')
        return self.func(*args, **kwargs)
    def __get__(self, instance, owner):     # При обращении к методам классов
        # print("tracer get:", self, instance, owner)
        return wrapper(self, instance)

class wrapper:    # Сохраняет оба экземпяра
    def __init__(self, desc, subj):
        # print("wrapper init:", desc, subj)
        self.desc = desc
        self.subj = subj
    def __call__(self, *args, **kwargs):    # Делегирует вызов дескриптору
        # print("wrapper call")
        return self.desc(self.subj, *args, **kwargs)

class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
    @tracer
    def lastName(self):
        return self.name.split()[-1]
    @tracer
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))

print('-' * 40)
func('a', 'b', 'c')     # wrapper('a', 'b', 'c')
func(a=1, b=2, c=3)
print(spam(2, 4))
print(spam(4, y=2))
tmp = spam(2, 8)
print(tmp)
print("Methods...")
bob = Person("Bob Smith", 100000)
sue = Person("Sue Jones", 50000)
print(bob.name, sue.name)
sue.giveRaise(.10)          # Вызовет sue.giveRaise.__get__ => wrapper.__call__ => tracer.__call__
print()
print(bob.pay, sue.pay)
print(bob.lastName())
print(sue.lastName())
print('-' * 40)


class tracer:
    def __init__(self, func):
        # print("tracer init:", func)
        self.func = func
        self.calls = 0
    def __call__(self, *args, **kwargs):
        # print("tracer call")
        self.calls += 1
        res = ", ".join([str(x) for x in args])
        if args and kwargs:
            res += ", "
        res += ", ".join(["{}={}".format(k, v) for k, v in kwargs.items()])
        print("call #{0} to {1}({2}) => ".format(self.calls, self.func.__name__, res), end='')
        return self.func(*args, **kwargs)
    def __get__(self, instance, owner):
        # print("tracer get:", self, instance)
        def wrapper(*args, **kwargs):
            # print("wrapper")
            return self(instance, *args, **kwargs)      # Приведет к вызвову tracer.__call__
        return wrapper

@tracer             # Может применяться к функциям
def func(a, b, c):      # func = Tracer(func)
    print(a + b + c)
@tracer
def spam(x, y):
    return x ** y

class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
    @tracer
    def lastName(self):
        return self.name.split()[-1]
    @tracer
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))

print('-' * 40)
func('a', 'b', 'c')     # wrapper('a', 'b', 'c')
func(a=1, b=2, c=3)
print(spam(2, 4))
print(spam(4, y=2))
tmp = spam(2, 8)
print(tmp)
print("Methods...")
bob = Person("Bob Smith", 100000)
sue = Person("Sue Jones", 50000)
print(bob.name, sue.name)
sue.giveRaise(.10)          # Вызовет sue.giveRaise.__get__ => wrapper.__call__ => tracer.__call__
print()
print(bob.pay, sue.pay)
print(bob.lastName())
print(sue.lastName())
print('-' * 40)