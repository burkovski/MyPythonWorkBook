def decorator(F):       # Перехватит вызов декорируемой ф-ции
    print("It's decorator of {0}()".format(F.__name__))
    return F            # Веренет оригинальную декорируемую ф-цию

@decorator
def myfunc():
    print("In myfunc")
myfunc()


def decorator(F):           # Перехватит вызов декорируемой ф-ции
    def wrapper(*args):     # Обертывающая функция
        print(tuple(reversed(args)))
        F(*args)            # Вызвов оригинальной функции
    return wrapper          # Присвоит ориг. ф-ции новую логику

@decorator
def func(*args):        # func предается декоратору в аргументе F
    print(args)

func(1, 2, 3.14, "four")    # В действительности будет вызвана функция wrapper

class C:
    @decorator
    def method(self, x, y):
        print(x, y)
X = C()
X.method(1, 2)          # В дейсвительности - wrapper(X, 1, 2)


class decorator:            # Тоже самое, на основе классов, непригоден для декорирования методов
    def __init__(self, func):   # На этапе декорирования @
        self.func = func    # Сохранит оригинальную ф-цию в атрибуте экземпляра
    def __call__(self, *args):      # Вызывается выражением func()
        print(tuple(reversed(args)))
        self.func(*args)            # Вызов декорируемой ф-ции

@decorator
def func(*args):
    print(args)

func(1, 2, 3.14, "four")




def decorator(cls):        # На этапе декорирования @
    class Wrapper:
        def __init__(self, *args):      # На этапе создания экземпляра
            self.wrapped = cls(*args)
        def __getattr__(self, item):    # Вызывается при обращении к атрибуту
            return getattr(self.wrapped, item)
    return Wrapper

@decorator      # C = decorator(C)
class C:        # Тепер, при обращении к C - вызывается Wrapper
    def __init__(self, x, y):       # Вызывается методом Wrapped.__init__
        self.attr = "spam"
        self.data = x, y

X = C(2, 3.14)              # В действительности - вызовет Wrapped(2, 3.14)
print(X.attr, X.data)
Y = C('a', 'bc')
print(Y.wrapped.__dict__)


class Decorator:
    def __init__(self, C):      # На этапе декорирования @
        self.C = C
    def __call__(self, *args):      # При создании экземпляра
        self.wrapped = self.C(*args)
        return self        # Вернуть self.wrapped для уникальности экземпляров декоратора
    def __getattr__(self, item):    # Вызыватся при обращении к атрибуту
        print("GETATTR")
        return getattr(self.wrapped, item)

@Decorator
class C:        # C = Decorator(C)
    def __init__(self, val):
        self.data = val

X = C(123)
Y = C(321)      # Затрет X, если __call__ возвращает self
print(X.data)
print(Y.data)
print('=' * 50)


def dec1(F):
    print("decorator #1 =>", F())
    return lambda: 'X' + F()


def dec2(F):
    print("decorator #2 =>", F())
    return lambda: 'Y' + F()


def dec3(F):
    print("decorator #3 =>", F())
    return lambda: 'Z' + F()


@dec1
@dec2
@dec3
def func():         # func = dec1(dec2(dec3(func)))
    return "spam"


# func = dec1(dec2(dec3(func)))

print("func call:", func())
