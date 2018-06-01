def Tracer(aClass):         # На этапе декорирования
    class Wrapper:
        def __init__(self, *args, **kwargs):    # На этапе создания экземпляра
            self.fetches = 0
            self.wrapped = aClass(*args, **kwargs)      # Использует имя в объемлющей области видимости
        def __getattr__(self, item):
            print("Trace: {}".format(item))             # Перехватывает обращения ко всем атрибутам, кроме своих
            self.fetches += 1
            return getattr(self.wrapped, item)          # Делегирует обращения обернутому объекту
    return Wrapper

@Tracer
class Spam:                 # Имени Spam присваетвается экземпляр Wrapper
    @staticmethod
    def display():
        print("SPAM" * 8)

@Tracer
class Person:               # Person = Tracer(Person)
    def __init__(self, name, hours, rate):
        self.name = name
        self.hours = hours
        self.rate = rate
    def pay(self):          # Доступ извне перехватывается
        return self.hours * self.rate   # Изнутри - не перехватывается

food = Spam()                   # Вызовет Wrapper()
food.display()                  # Вызовет __getattr__
print([food.fetches])
bob = Person("Bob", 40, 50)
print(bob.name)
print(bob.pay())
print()
sue = Person("Sue", 100, 60)
print(sue.name)
print(sue.pay())
print(bob.name)
print(bob.pay())
print([bob.fetches, sue.fetches])


@Tracer
class MyList(list): pass        # MyList = Tracer(MyList)
X = MyList([1, 2, 3])           # Вызовет Wrapper()
X.append(4)                     # Вызовет __getattr__, append
print(X.wrapped)

WrapList = Tracer(list)         # Декорирование выполняется вручную
X = WrapList([4, 5, 6])         
X.append(7)
print(X.wrapped)