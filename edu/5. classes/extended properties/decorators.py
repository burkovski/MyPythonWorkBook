class C:
    @staticmethod   # Синтаксис декорирования
    def meth():
        ...

class C1:
    def meth():
        ...
    meth = staticmethod(meth)   # Повтороное присваивание



class Tracer:
    def __init__(self, func):
        self.calls = 0
        self. func = func
    def __call__(self, *args):
        self.calls += 1
        print("call <{0}> to {1}()".format(self.calls, self.func.__name__))
        self.func(*args)    # Вызов оригинальной функции

@Tracer             # То же, что и spam = Tracer(spam)
def spam(a, b, c):  # Оберывает spam в объект - декоратор
    print(a, b, c)

spam(1, 2, 3)           # В действительности вызывается объект-обертка
spam('a', 'b', 'c')     # То есть, вызывается метод __call__ в классе
spam(4, 5, 6)           # Метод __call__ выполняет дополнительные действия и вызывает оригинальную функцию



def decorator(aClass): ...      # Функция-декоратор

@decorator          # Непосредственно, вызов декоратора
class C: ...

class C: ...
C = decorator(C)    # Эквивалент выражения


def count(aClass):
    aClass.numInstance = 0
    return aClass           # Возвражает сам класс с атрибутом numInstance, а не обертку

@count
class Spam: ...         # То же, что и Spam = count(Spam)

@count
class Sub(Spam): ...    # Инструкция numInstance в классах больше не нужна

@count
class Other(Spam): ...

print(Sub.__dict__)
