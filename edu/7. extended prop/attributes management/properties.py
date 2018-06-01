class Person:
    def __init__(self, name):
        self._name = name
    def getName(self):
        print('fetch...')
        return self._name
    def setName(self, value):
        print("change...")
        self._name = value
    def delName(self):
        print("remove...")
    def __str__(self):
        return "name: {}".format(self.getName())
    name = property(getName, setName, delName, "name property docs")

bob = Person("Bob Smith")   # Объект bob имеет управляемый атрибут
print(bob.name)             # Вызовет getName
bob.name = "Bob Stolone"    # Вызовет setName
print(bob.name)
del bob.name                # Вызовет delName
print('-' * 20)
sue = Person("Sue Jones")   # Объект sue также наследует свойство
print(sue.name)
print(Person.name.__doc__)  # Строка документирования
print()



class Person:
    def __init__(self, name):
        self._name = name
    @property           # name = property(name)
    def name(self):
        """name property docs"""
        print("fetch...")
        return self._name
    @name.setter        # name = name.setter(name)
    def name(self, value):
        print("change...")
        self._name = value
    @name.deleter       # name = name.deleter(name)
    def name(self):
        print("remove...")

bob = Person("Bob Smith")   # Объект bob имеет управляемый атрибут
print(bob.name)             # Вызовет метод getter свойства name (name1)
bob.name = "Bob Stolone"    # Вызовет метод setter свойства name (name2)
print(bob.name)
del bob.name                # Вызвовет метод deleter свойства name (name3)
print('-' * 20)
sue = Person("Sue Jones")   # Объект sue также наследует свойство
print(sue.name)
print(Person.name.__doc__)  # Или: help(Person.name)
print()


class propSquare:
    def __init__(self, value):
        self.value = value
    def getX(self):
        return "{0} ** 2 = {1}".format(self.value, self.value ** 2)
    def setX(self, new_value):
        self.value = new_value
    X = property(getX, setX)

print("-" * 15)
Q = propSquare(3)
R = propSquare(32)
print(Q.X)
Q.X = 4
print(Q.X)
print(R.X)
print("-" * 15)


class PropSquare:
    def __init__(self, value):
        self.value = value
    @property
    def X(self):
        return "{0} ** 2 = {1}".format(self.value, self.value ** 2)
    @X.setter
    def X(self, new_value):
        self.value = new_value

Q = PropSquare(3)
R = PropSquare(32)
print(Q.X)
Q.X = 4
print(Q.X)
print(R.X)
print("-" * 15)