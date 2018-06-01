def result(dec):
    print(dec)
    @dec
    class Person:
        def __init__(self, name, hours, rate):
            self.name = name
            self.hours = hours
            self.rate = rate

        def pay(self):
            return self.rate * self.hours

    @dec
    class Spam:
        def __init__(self, val):
            self.attr = val

    bob = Person("Bob", 40, 10)
    print(bob.name, bob.pay())
    sue = Person("Sue", 50, 20)
    print(sue.name, sue.pay())
    X = Spam(42)
    Y = Spam(99)
    print(X.attr, Y.attr)

instances = {}
def getInstance(aClass, *args):     # Управялет глобальной таблицей
    if aClass not in instances:     # По одному элементу словаря для каждого класса
        instances[aClass] = aClass(*args)
    return instances[aClass]

def singleton(aClass):      # На этапе декорирования
    def onCall(*args):      # На этапе создания экземпляра
        return getInstance(aClass, *args)
    return onCall
result(singleton)


def singleton(aClass):          # На этапе декорирования
    instance = None
    def onCall(*args):          # На этапе создания экземпялра
        nonlocal instance       # У кажого класса - свой уникальный экземпляр
        if instance is None:
            instance = aClass(*args)
        return instance         # По одной области видимости на каждый класс
    return onCall
result(singleton)


class singleton:
    def __init__(self, aClass):     # На этапе декорирования
        self.aClass = aClass
        self.instance = None
    def __call__(self, *args):          # На этапе создания экземпяра
        if self.instance is None:       # По одному экземпяру на класс
            self.instance = self.aClass(*args)
        return self.instance
result(singleton)