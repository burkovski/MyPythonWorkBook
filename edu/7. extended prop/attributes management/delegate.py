class GetAttr:
    eggs = 88
    def __init__(self):
        self.spam = 77
    def __len__(self):
        print("__len__: 42")
        return 42
    def __getattr__(self, item):
        print("getattr:", item)
        if item == "__str__":
            return lambda *args: "[Getattr Str]"
        else:
            return lambda *args: None

class GetAttribute:
    eggs = 88
    def __init__(self):
        self.spam = 77
    def __len__(self):
        print("__len__: 42")
        return 42
    def __getattribute__(self, item):
        print("getattribute:", item)
        if item == "__str__":
            return lambda *args: "[GetAttribute Str]"
        else:
            return lambda *args: None

for Class in (GetAttr, GetAttribute):
    print('\n' + Class.__name__.ljust(50, '='))

    X = Class()
    X.eggs
    X.spam
    X.other
    len(X)

    try:
        X[0]
    except:
        print("fail []")

    try:
        X + 99
    except:
        print("fail +")

    try:
        X()
    except:
        print("fail ()")

    print(X.__str__())
    print(X)
print('\n')



class Person:
    def __init__(self, name, job=None, pay=0):
        self.name = name
        self.job = job
        self.pay = pay
    def lastName(self):
        return self.name.split()[-1]
    def giveRaise(self, percent):
        self.pay = int(self.pay * (1 + percent))
    def __str__(self):
        return "[Person: {0}, {1}]".format(self.name, self.job)

class Manager:
    def __init__(self, name, pay):
        self.person = Person(name, "mgr", pay)
    def giveRaise(self, percent, bonus=0.10):
        self.person.giveRaise(percent+bonus)
    def __getattr__(self, item):
        return getattr(self.person, item)
    def __str__(self):
        return str(self.person)

sue = Person("Sue Jones", job="dev", pay=100000)
print(sue.lastName())
sue.giveRaise(.10)
print(sue)
tom = Manager('Tom Jones', 50000)   # Manager.__init__
print(tom.lastName())               # Manager.__getattr__ -> Person.lastName
tom.giveRaise(.10)                  # Manager.giveRaise -> Person.lastName
print(tom)                          # Manager.__str__ -> Person.__str__
print('-' * 45)


class Manager:
    def __init__(self, name, pay):
        self.person = Person(name, "mgr", pay)      # Встроеный объект Person
    def giveRaise(self, percent, bonus=0.10):
        self.person.giveRaise(percent+bonus)        # Перехватывает и делегирует
    def __getattribute__(self, item):
        print('**', item)
        if item in ("person", "giveRaise"):
            return object.__getattribute__(self, item)      # Возвращает свой атрибут
        else:
            return getattr(self.person, item)           # Делегирует остальне атрибуты
    def __str__(self):
        return str(self.person)

sue = Person("Sue Jones", job="dev", pay=100000)
print(sue.lastName())
sue.giveRaise(.10)
print(sue)
tom = Manager('Tom Jones', 50000)
print(tom.lastName())
tom.giveRaise(.10)
print(tom)
print('-' * 45)

class Manager:
    def __init__(self, name, pay):
        self.person = Person(name, "mgr", pay)
    def __getattribute__(self, item):
        print("**", item)
        person = object.__getattribute__(self, 'person')
        if item == "giveRaise":
            return lambda percent: person.giveRaise(percent+.10)
        else:
            return getattr(person, item)
    def __str__(self):
        person = object.__getattribute__(self, 'person')
        return str(person)

sue = Person("Sue Jones", job="dev", pay=100000)
print(sue.lastName())
sue.giveRaise(.10)
print(sue)
tom = Manager('Tom Jones', 50000)
print(tom.lastName())
tom.giveRaise(.10)
print(tom)