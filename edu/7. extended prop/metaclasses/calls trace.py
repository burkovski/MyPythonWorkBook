from types import FunctionType
from mytools import tracer, timer

class MetaTrace(type):
    def __new__(mcs, cls_name, sprs, cls_dict):
        for attr, attrval in cls_dict.items():
            if type(attrval) is FunctionType:               # Метод?
                cls_dict[attr] = tracer(attrval)            # Декорировать
        return type.__new__(mcs, cls_name, sprs, cls_dict)  # Создать класс

class Person(metaclass=MetaTrace):
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
    def giveRaise(self, percent):
        self.pay += int(self.pay * percent)
    def lastName(self):
        return self.name.split()[-1]

bob = Person("Bob Smith", 100000)
sue = Person("Sue Smith", 50000)
print(bob.name, sue.name)
bob.giveRaise(.10)
print(bob.pay)
print(bob.lastName(), sue.lastName())
print("=" * 20)


def decorateAll(dec):
    class MetaTrace(type):
        def __new__(mcs, cls_name, sprs, cls_dict):
            for attr, attrval in cls_dict.items():
                if type(attrval) is FunctionType:  # Метод?
                    cls_dict[attr] = dec(attrval)  # Декорировать
            return type.__new__(mcs, cls_name, sprs, cls_dict)  # Создать класс
    return MetaTrace

class Person(metaclass=decorateAll(tracer)):
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
    def giveRaise(self, percent):
        self.pay += int(self.pay * percent)
    def lastName(self):
        return self.name.split()[-1]

bob = Person("Bob Smith", 100000)
sue = Person("Sue Smith", 50000)
print(bob.name, sue.name)
bob.giveRaise(.10)
print(bob.pay)
print(bob.lastName(), sue.lastName())
print("=" * 20)


def decorateAll(decorator):
    def decoDecorate(aClass):
        for attr, attrval in aClass.__dict__.items():
            if type(attrval) is FunctionType:
                setattr(aClass, attr, decorator(attrval))   # Не __dict__
        return aClass
    return decoDecorate

@decorateAll(tracer)
class Person:
    def __init__(self, name, pay):
        self.name = name
        self.pay = pay
    def giveRaise(self, percent):
        self.pay += int(self.pay * percent)
    def lastName(self):
        return self.name.split()[-1]

bob = Person("Bob Smith", 100000)
sue = Person("Sue Smith", 50000)
print(bob.name, sue.name)
bob.giveRaise(.10)
print(bob.pay)
print(bob.lastName(), sue.lastName())
