# Тррассировка вызовов, с помощью метакласса
def Tracer(cls_name, sprs, cls_dict):   # На этапе создания класса
    aClass = type(cls_name, sprs, cls_dict)     # Создать клиентский класс
    class Wrapper:
        def __init__(self, *args, **kwargs):    # На этапе создания экземпляра
            self.wrapped = aClass(*args, **kwargs)
        def __getattr__(self, item):
            print("Trace:", item)      # Перехватит все обращения, кроме .wrapped
            return getattr(self.wrapped, item)      # Делегирует обращение обернутому объекту
    return Wrapper

class Person(metaclass=Tracer):     # Создать класс Person с метаклассом Tracer
    def __init__(self, name, hours, rate):      # Wrapper запоминате Person
        self.name = name
        self.hours = hours
        self.rate = rate        # Доступ изнути не трассируется
    def pay(self):
        return self.hours * self.rate

bob = Person("Bob", 40, 50)     # bob - в действительности экземпляр Wrapper
print(bob.name)                 # экземпляр Person встривается во Wrapper
print(bob.pay())                # вызовет __getattr__
print(type(Person))