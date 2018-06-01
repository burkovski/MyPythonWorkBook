class Descriptor:
    def __get__(self, instance, owner):
        print(self, instance, owner, sep='\n')

class Subject:
    attr = Descriptor()     # Атрибут класса - экземпляр класса Descriptor

print('-' * 42)
X = Subject()
X.attr      # X.attr -> Descriptor.__get__(Subject.attr, X, Subject)
print()
Subject.attr    # X.Subject -> Descriptor.__get__(Subject.attr, None, Subject)
print('-' * 42)


class D:
    def __get__(self, instance, owner):
        print("get...")

class C:
    a = D()     # Дескриптор

X = C()
X.a             # Вызовет D.__get__(C.a, X, C)
C.a
X.a = 99        # Сохранит значение в X, отключит дескриптор C.a
print(X.a)
print(X.__dict__)
Y = C()
Y.a             # Y также унаследует дескриптор


class D:
    def __get__(self, instance, owner):
        print("get...")
    def __set__(self, instance, value):
        raise AttributeError("cannot set")

class C:
    a = D()     # Дескриптор => атрибут только для чтения

X = C()
X.a
# X.a = 99        # Атрибут только для чтения
print('-' * 20)



class Name:
    """Name descriptor docs"""
    def __get__(self, instance, owner):     # self - экземпялр класса Name
        print("fetch...")                   # instance - экземпляр класса Person
        return instance._name               # owner - класс Person
    def __set__(self, instance, value):
        print("change...")
        instance._name = value
    def __delete__(self, instance):
        print("remove...")
        del instance._name

class Person:
    def __init__(self, name):
        self._name = name
    name = Name()               # Присвоить атрибуту дескриптор

bob = Person("Bob Smith")       # Объект bob
print(bob.name)                 # Вызовет Name.__get__
bob.name = "Bob Stolone"        # Вызовет Name.__set__
print(bob.name, '\n')
del bob.name                    # Вызовет Name.__delete__
sue = Person("Sue Jones")
print(sue.name)
print(Name.__doc__)             # Или help(Name)
print('-' * 20)



class Person:
    def __init__(self, name):
        self._name = name

    class Name:         # Вложенный класс
        """Name descriptor docs"""
        def __get__(self, instance, owner):  # self - экземпялр класса Name
            print("fetch...")  # instance - экземпляр класса Person
            return instance._name  # owner - класс Person

        def __set__(self, instance, value):
            print("change...")
            instance._name = value

        def __delete__(self, instance):
            print("remove...")
            del instance._name

    name = Name()               # Присвоить атрибуту дескриптор

bob = Person("Bob Smith")       # Объект bob
print(bob.name)                 # Вызовет Name.__get__
bob.name = "Bob Stolone"        # Вызовет Name.__set__
print(bob.name, '\n')
del bob.name                    # Вызовет Name.__delete__
sue = Person("Sue Jones")
print(sue.name)
print(Person.Name.__doc__)      # Изменено: имя Name больше не доступно за пределами класса
print('-' * 20)


class DescSquare:
    def __init__(self, value):              # Кажый дескриптор имеет свои данные
        self.value = value
    def __get__(self, instance, owner):     # Операция получения значения
        return self.value ** 2
    def __set__(self, instance, value):     # Операция присваивания
        self.value = value

class Client1:
    X = DescSquare(4)       # Присвоить экземпляр дескриптора атрибуту класса
class Client2:
    X = DescSquare(32)      # Другой экземпляр в другом классе, также можно было создать два экз. в ожном кдассе

c1 = Client1()
c2 = Client2()
print(c1.X)
c1.X = 3
print(c1.X)
print(c2.X)


class DescState:                        # Дескриптор использует собственный атрибут
    def __init__(self, value):
        self.value = value
    def __get__(self, instance, owner):
        print("DescState get")
        return self.value * 10
    def __set__(self, instance, value):
        print("DescState set")
        self.value = value

class Client:
    X = DescState(2)            # Дескриптор использует атрибут класса
    Y = 3                       # Атрибут класса
    def __init__(self):
        self.Z = 4              # Атрибут экземпляра

print('-' * 20)
obj = Client()
print(obj.X, obj.Y, obj.Z)
obj.X, obj.Y, obj.Z = 5, 6, 7
print(obj.X, obj.Y, obj.Z, '\n')


class InstState:                # Дескриптор использует атрибут экземпляра
    def __get__(self, instance, owner):
        print("Instance get")
        return instance._Y  * 100    # Предполагает наличие атрибута в клиентском классе
    def __set__(self, instance, value):
        print("Instance get")
        instance._Y = value

class Client:
    X = DescSquare(2)   # Дескриптор атрибута класса
    Y = InstState()     # Дескриптор атрибута класса
    def __init__(self):
        self._Y = 3     # Атрибут экземпляра
        self.Z = 4      # Атрибут экземпляра

obj = Client()
print(obj.X, obj.Y, obj.Z)
obj.X, obj.Y, obj.Z = 5, 6, 7
print(obj.X, obj.Y, obj.Z)
