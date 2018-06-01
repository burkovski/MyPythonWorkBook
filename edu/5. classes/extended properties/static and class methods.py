class Spam:
    numInstance = 0
    def __init__(self):
        Spam.numInstance += 1
    def printNumInstance():     # Не ожидает получить ссылку на атрибут - вызов только через имя класса
        print("Number of instances created:", Spam.numInstance)

a = Spam()
b = Spam()
c = Spam()
# c.printNumInstance()      # <= Ошибка: метод не ожидает получить аргумент - получает self
Spam.printNumInstance()     # Работает в 3.Х - вызвов функции из класса, в 2.Х - ошибка(несвязаный метод без self)
print()


def printNumInstance():     # Обычная функция в роли статического метода
    print("Number of instances created:", Spam.numInstance)

class Spam:
    numInstance = 0
    def __init__(self):
        Spam.numInstance += 1

a = Spam()
b = Spam()
c = Spam()
printNumInstance()
print()


class Spam:
    numInstance = 0
    def __init__(self):
        Spam.numInstance += 1
    def printNumInstance(self):     # Не ожидает получить ссылку на атрибут - вызов только через имя класса
        print("Number of instances created:", Spam.numInstance)

a = Spam()
b = Spam()
c = Spam()
a.printNumInstance()
Spam.printNumInstance(a)
Spam().printNumInstance()   # Эта попытка извлечь счетчик изменяет его
print()


class Methods:
    def instance_method(self, x):   # Обычный метод экземпляра
        print(self, x)
    def static_method(x):        # Статический метод: экземпляр не передается
        print(x)
    def class_method(cls, x):       # Метод класса: получает класс, но не экземпяр
        print(cls, x)

    static_method = staticmethod(static_method)     # Сделать static_method метод статическим
    class_method = classmethod(class_method)        # Сделать class_method методом класса

obj = Methods()         # Создать экземпляр
obj.instance_method(1)           # Обычный вызов, через экземпляр => instance_method(obj, 2)
Methods.instance_method(obj, 2)  # Обычный вызов через имя класса => экзепляр передается явно
Methods.static_method(3)    # Вызов статического метода, через имя класса, экземпляр не передается и не ожидется
obj.static_method(4)        # Вызов статического метода, через экземпляр, экземпляр не пережается и не ожижается
Methods.class_method(5)     # Вызов метода класса через имя класса => class_method(Methods, 5)
obj.class_method(6)         # Вызов метода класса через экземпляр  => class_method(Methods, 6)
print()


class Spam:                 # Для доступа к данным класса используется статический метод
    numInstance = 0
    def __init__(self):
        Spam.numInstance += 1
    def printNumInstance():
        print("Number of instances:", Spam.numInstance)
    printNumInstance = staticmethod(printNumInstance)

a = Spam()
b = Spam()
c = Spam()
Spam.printNumInstance()     # Вызывается, как простая функция
a.printNumInstance()        # Аргумент с экземпляром не передается
print()

class Sub(Spam):
    def printNumInstance():         # Переодперделяет статический метод
        print("Extra stuff...")
        Spam.printNumInstance()     # Который вызывает оригинал
    printNumInstance = staticmethod(printNumInstance)

x = Sub()
y = Sub()
x.printNumInstance()        # Вызов через экземпляр подкласса
Sub.printNumInstance()      # Вызов через имя подкласса
print()

class Other(Spam):      # Наследует оригинальный статический метод
    pass

c = Other()
c.printNumInstance()        # Вызов через экземпляр
Other.printNumInstance()    # Вызвов через имя подкласса
print()


class Spam:                 # Вместо стаического метода используется метод класса
    numInstance = 0
    def __init__(self):
        Spam.numInstance += 1
    def printNumInstance(cls):
        print("Number of instances:", cls.numInstance, cls)
    printNumInstance = classmethod(printNumInstance)

a, b = Spam(), Spam()
a.printNumInstance()        # В первом аргументе передается класс
Spam.printNumInstance()     # Также, в первом аргументе передается класс
print()


class Sub(Spam):
    def printNumInstance(cls):
        print("Extra stuff...", cls)
        Spam.printNumInstance()         # Вызов относительно Spam => в агрументе передается Spam
    printNumInstance = classmethod(printNumInstance)

class Other(Spam):
    pass

x, y, z = Sub(), Spam(), Other()
x.printNumInstance()        # Вызов через экземпляр подкласса
Sub.printNumInstance()      # Вызов через сам подкласс
y.printNumInstance()        # Вызов через экземпляр класса
Spam.printNumInstance()     # Вызов через сам класс
z.printNumInstance()        # В аргументе cls передается Other
print()


class Spam:
    numInstances = 0        # Счетчик экземпляров для каждого класса
    def count(cls):
        cls.numInstances += 1   # cls - ближайший к экземпляру класс в дереве наследования
    def __init__(self):
        self.count()            # Передаст self.__class__ в cls для подсчета
    count = classmethod(count)

class Sub(Spam):
    numInstances = 0
    def __init__(self):        # Переопределяет __init__
        super().__init__()

class Other(Spam):          # Наследует __init__
    numInstances = 0

x = Spam()
y1, y2 = Sub(), Sub()
z1, z2, z3 = Other(), Other(), Other()
print(x.numInstances, y1.numInstances, z1.numInstances)
print(Spam.numInstances, Sub.numInstances, Other.numInstances)