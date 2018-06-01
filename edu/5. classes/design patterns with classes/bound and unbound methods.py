class Spam:
    def doit(self, massage):
        print(massage)

object = Spam()
object.doit("Hello world! [1]")
x = object.doit         # Экземляр связанного метода: экземпляр+функция
x("Hello world! [2]")   # То же, что и object.doit(...)

t = Spam.doit                   # Объект несвязанного метода
t(object, "Hello world! [3]")   # Требует явно передать экземпляр
print()


class Eggs:
    def m1(self, n):
        print(n)
    def m2(self):
        x = self.m1  # Объект связанного метода | x = Eggs().m1 - несвязанного
        x(42)        # Выгдядит, как обычная функция

Eggs().m2()
print()


class SelfLess:
    def __init__(self, data):
        self.data = data
    # @staticmethod
    def selfless(arg1, arg2):   # Простая фукция в классе (Python 3.Х)
        return arg1 + arg2
    def normal(self, arg1, arg2):
        return self.data + arg1 + arg2

X = SelfLess(2)
print(X.normal(3, 4))               # Экземпляр передается автоматически
print(SelfLess.normal(X, 3, 4))     # Метод ожидает получить self: передается вручную
print(SelfLess.selfless(4, 5))      # Вызов без экземпляра(не ожидается) - ошибка в 2.Х
print()


class Number:
    def __init__(self, base):
        self.base = base
    def double(self):
        return self.base * 2
    def triple(self):
        return self.base * 3

x = Number(2)   # Объекты экземпляров класса
y = Number(3)   # Атрибуты + методы
z = Number(4)
print(x.double())   # Обычный непосредственный метод
acts = [x.double, y.double, y. triple, z.double]    # Список связаных методов
for act in acts:                                    # Вызовы откладываются
    print(act())                                    # Вызов как функции

bound = x.double
print(bound.__self__, bound.__func__)
print(bound())  # Вызовет bound.__func__(bound.__self__)
print()


def square(arg):    # Простая функция
    return arg ** 2

class Sum:          # Вызываемые экземпляры
    def __init__(self, val):
        self.val = val
    def __call__(self, arg):
        return self.val * arg

class Product:      # Связанные экземпляры
    def __init__(self, val):
        self.val = val
    def method(self, arg):
        return self.val * arg

sobject = Sum(2)
pobject = Product(3)
acts = [square, sobject, pobject.method]    # Функция, экземпляр, метод
for act in acts:    # Все три вызываются одинаково
    print(act(5))   # Вызов любого вызываемого с одним аргументом
print([act(5) for act in acts])                 # Генераторы, отображения
print(list(map(lambda act: act(5), acts)))