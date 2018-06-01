"""
Декораторты Private и Public для объявления частных и общедоступных атриубов.
Управляют доступом к атрибутам, хранящимся в экземпялре или наследуемым
от классов. Декоратор Private объявляет атрибуты, ктотрые недоступны за
пределами декорируемого класса, а декоратор Public объявляет все атрибуты,
которые, наоборот, доступны.
"""

traceMe = False
def trace(*args):
    if traceMe: print("[{0}]".format(' '.join(map(str, args))))

def accessControl(fail_if):
    def onDecorator(aClass):
        class onInstance:
            def __init__(self, *args, **kwargs):
                self.__wrapped = aClass(*args, **kwargs)
            def __getattr__(self, item):
                trace('get:', item)
                if fail_if(item):
                    raise TypeError("private attribute fetch: " + item)
                else:
                    return getattr(self.__wrapped, item)
            def __setattr__(self, key, value):
                trace('set:', key, value)
                if key == "_onInstance__wrapped":
                    self.__dict__[key] = value
                elif fail_if(key):
                    raise TypeError("private attribute change: " + key)
                else:
                    setattr(self.__wrapped, key, value)
        return onInstance
    return onDecorator

def Private(*attributes):
    return accessControl(fail_if=(lambda attr: attr in attributes))

def Public(*attributes):
    return accessControl(fail_if=(lambda attr: attr not in attributes))


if __name__ == "__main__":
    traceMe = True
    @Private('age')
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    X = Person("Bob", 40)
    print(X.name)
    X.name = "Sue"

    @Public('name')
    class Person:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    X = Person("Bob", 40)
    print(X.name)