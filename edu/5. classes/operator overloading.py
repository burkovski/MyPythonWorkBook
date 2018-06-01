class Number:
    def __init__(self, val):
        self.data = val

    def __sub__(self, other):   # Для выражений экземпляр - other
        return Number(self.data - other)    # Результат - новый экземпляр

    def __add__(self, other):   # Для выражений экземпляр + other
        return Number(self.data + other)

X = Number(5)   # X.data = 5
Y = X - 2       # X.data - 2 = Y.data | Y = Number(5 - 2) -> Y.data = 3
print(Y.data)   # Y.data = 3
Z = Y + 4       # Y.data + 3 = Z.data | Z = Number(4 + 3) -> Z.data = 7
print(Z.data)   # Z.data = 7
print()


class Indexer:
    data = [x for x in range(5, 10)]
    def __getitem__(self, index):       # Вызывается при идексации или извлечениий среза экземпляра
        print("getitem: {}".format(index))
        res = self.data[index]
        print("value: {}\n".format(res))

X = Indexer()
X[0]
X[2:5]


# Итерация идексированием
class Stepper:
    def __init__(self, value):
        self.data = value

    def __getitem__(self, i):
        return self.data[i]

X = Stepper("Spam")
for item in X:      # Цикл for вызывает метод __getitem__
    print(item, end=' ')
print()
print([x for x in X])
print(list(map(str.upper, X)))
a, b, *c = X
print(a, b, c)
print(list(X), tuple(X), ''.join(X), sep='; ')


# Протокол итераций
class Squares:
    def __init__(self, start, stop):
        self.value = start - 1
        self.stop = stop

    def __iter__(self):     # Возвращает итератор в iter()
        return self

    def __next__(self):     # Возвращает квадрат, на каждой итерации вызывается функцией next()
        if self.value == self.stop:
            raise StopIteration
        self.value += 1
        return self.value ** 2

for i in Squares(1, 5):     # for вызывает iter(), который вызывает __iter__()
    print(i, end=' ')       # На каждой итерации вызвается __next__()
print()
print([x for x in Squares(1, 5)], '\n')


# Несколько итератров в одном объекте
class SkipIterator:
    def __init__(self, wrapped):
        self.wrapped = wrapped      # Информация о состоянии
        self.offset = 0

    def __next__(self):
        if self.offset >= len(self.wrapped):    # Завершить итерации
            raise StopIteration
        else:
            item = self.wrapped[self.offset]    # Иначе перещагнуть вперед
            self.offset += 2
            return item

class SkipObject:
    def __init__(self, wrapped):    # Сохранить используемый элемент
        self.wrapped = wrapped

    def __iter__(self):         # Каждый раз инициалтзировать новый итератор
        return SkipIterator(self.wrapped)

alpha = "abcdef"
skipper = SkipObject(alpha)     # Создать объект-контейнер
for x in skipper:
    for y in skipper:
        print(x + y, end='; ')
print()


class Iters:
    def __init__(self, value):
        self.data = value

    def __getitem__(self, i):                       # Крайний случай для итераций
        print("get[{0}]:".format(i), end='')     # А также для индексирования и срезов
        return self.data[i]

    def __iter__(self):             # Предпочтительный для итераций
        print("iter=>", end='')     # Возможен только один активный итератор
        self.ix = 0
        return self

    def __next__(self):
        print("next:", end='')
        if self.ix == len(self.data): raise StopIteration
        item = self.data[self.ix]
        self.ix += 1
        return item

    def __contains__(self, item):   # Пердпочтительный для оператора in
        print("contains:", end='')
        return item in self.data

print()
X = Iters([1, 2, 3, 4, 5])  # Создать экземпляр
print(3 in X)               # Проверка на вхождение, вызовет метод __contains__
for item in X:              # Циклы, вызывает методы __iter__ => __next__
    print(item, end=" | ")

print()
print([i ** 2 for i in X])  # Другие итерационные контексты
print(list(map(bin, X)))
I = iter(X)
while True:         # Обход вручную(именно так действуют другие итераионные контексты
    try:
        print(next(I), end=' @ ')
    except StopIteration:
        break
print()


class Empty:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, attrname):    # Вызывается при попытке извлечь НЕСУЩЕСТВУЮШИЙ атрибут экземпляра
        if attrname == "age":
            return 40
        else:
            raise AttributeError(attrname)

print()
X = Empty("Bob")
print(X.name)
print(X.age)
# print(X.job) <- AttributeError
print()


class AccessControl:
    def __setattr__(self, attr, value):     # Вызывается при ВСЕХ попыткахприсваиваиня атрибутам экземпляра
        if attr == "age":                   # если метод определен: self.attr = value -> self.__setattr__('attr', value)
            self.__dict__[attr] = value   # При self.attr = value - повторный вызов __setattr__ -> бесконечная рекурсия
        else:
            raise AttributeError(attr + " not allowed")

X = AccessControl()
X.age = 40      # Вызвовет метод __setattr__
# X.name = "Bob" <- AttributeError


# (!) Имитация частных атрибутов
class PrivateExc(Exception): pass

class Privacy:
    def __setattr__(self, attrname, value):     # Вызывается self.attrname = value
        if attrname in self.privates:
            raise PrivateExc(attrname, self)
        else:
            self.__dict__[attrname] = value # self.attrname = value вызовет зацикливание

class Test1(Privacy):
    privates = ["age"]

class Test2(Privacy):
    privates = ["name", "pay"]
    def __init__(self):
        self.__dict__["name"] = "Tom"

X = Test1()
Y = Test2()

X.name = "Bob"
# Y.name = "Sue"   <= Ошибка
Y.age = 30
# X.age = 40  <= Ошибка


# __repr__ и __str__
class Adder:
    def __init__(self, value=0):
        self.data = value

    def __add__(self, other):
        self.data += other

class AddRerp(Adder):
    def __repr__(self):     # Вызывается при оторажении, если не определен __str__
        return "addrepr({0})".format(self.data)


x = AddRerp(2)  # __init__
x + 1           # __add__
print(x)        # __repr__
print(str(x))   # __repr__
print(repr(x))  # __repr__
print()

class AddStr(Adder):
    def __str__(self):
        return "[Value: {0}]".format(self.data)

x = AddStr(3)
x + 1
print(x)        # __str__
print(str(x))   # __str__
print(repr(x))  # __repr__ (Не определен)
print()

class AddBoth(Adder):       # (!) Лучше использовать class AddBoth(AddStr, AddRepr)
    def __repr__(self):     # Срока програмного кода
        return "addrepr({0})".format(self.data)

    def __str__(self):      # Удобочитаемая строка
        return "[Value: {0}]".format(self.data)

x = AddBoth(4)
x + 1
print(x)        # __str__
print(str(x))   # __str__
print(repr(x))  # __repr__
print()


class Printer:
    def __init__(self, val):
        self.val = val

    def __str__(self):          # Используется для вывода самого экземпляра
        return str(self.val)    # Преобразует результат в строку

    def __repr__(self):         # При остуствии __str__ и для вложеных объектов вызывается __repr__
        return self.__str__()   # Вызывается метод __str__ => уменьшение избыточности кода


objs = [Printer(3), Printer(2)]
for x in objs:
    print(x)    # При выводе экземпляра будет вызван __str__, но не тогда, когда он вложен в список
print(objs)     # Экземпляр вложен в список => __repr__
print()


# __radd__ __iadd__
class Commuter:
    def __init__(self, val):
        self.val = val

    def __add__(self, other):
        print("add", self.val, other)
        return self.val + other

    def __radd__(self, other):
        print("radd", other, self.val)
        return other + self.val

x = Commuter(88)
y = Commuter(99)
print(x + 1)    # __add__: экземпляр + не_экземпляр
print(1 + y)    # __radd__: не_экземпляр + экземпляр
print(x + y)    # __add__: экземпляр + экземпляр
print()

class Commuter:     # Тип класса распространяется на результат
    def __init__(self, val):
        self.val = val

    def __add__(self, other):
        if isinstance(other, Commuter): other = other.val   # При сложении двух экземпляров - self.val + other.val
        return Commuter(self.val + other)

    def __radd__(self, other):
        return Commuter(other + self.val)

    def __iadd__(self, other):  # Реализует операцию x += y
        self.val += other
        return self

    def __str__(self):
        return "<Commuter: {0}>".format(self.val)

x = Commuter(88)
y = Commuter(99)
print(x + 10)    # Результат - экземпляр класса Commuter
print(10 + y)
print(x + y)     # Нет вложения - не проиходит рекурсивный вызов __radd__
x += 1
print(x)
print()


# __call__
class Callee:
    def __call__(self, *args, **kwargs):    # При вызове экземпляра как функции, в форме self()
        print("Called: {0}, {1};".format(args, kwargs))

C = Callee()
C(1, 2, 3)
C(1, 2, 3, x=4, y=5)
print()


# __bool__ __len__
class BoolLen:
    def __init__(self, data):
        self.data = data

    def __bool__(self):
        return bool(self.data)

    def __len__(self):
        return len(self.data)

X = BoolLen([1, 2, 3])
if X:
    print(len(X))