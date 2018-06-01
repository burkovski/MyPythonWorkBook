class Person:
    def __init__(self, name):
        self._name = name           # Также вызывает __setattr__

    def __getattr__(self, item):    # Вызвывается при obj.undefined
        if item == 'name':          # Для отсутствуещего атрибута с именем name
            print("fetch...")
            return self._name       # Не вызывает зацикливания: НЕсуществующий атрибут
        else:                       # Обращение к несуществующим атрибутам вызовет ошибку
            raise AttributeError(item)

    def __setattr__(self, key, value):  # Вызывается при obj.any = value
        if key == "name":
            print("change...")
            key = "_name"               # Внутренее имя атрибута
        self.__dict__[key] = value      # Предотвратить зацикливание

    def __delattr__(self, item):        # Вызывается при del obj.any
        if item == 'name':
            print("remove...")
            item = "_name"
        del self.__dict__[item]         # Удаление эдемента словаря не вызывает ошибку

bob = Person("Bob Smith")           # Объект bob обладает управляемым атрибутом
print(bob.name)                     # __getattr__
bob.name = "Robert Smith"           # __setattr__
print(bob.name, '\n')               # __getattr__
del bob.name                        # __delattr__
sue = Person("Sue Jones")           # __setattr__
print(sue.name)                     # __getattr__
print('-' * 20)


class AttrSquare:
    def __init__(self, value):
        self.value = value

    def __getattr__(self, item):
        if item == 'X':
            return self.value ** 2
        else:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        if key == 'X':
            key = "value"
        self.__dict__[key] = value

A = AttrSquare(3)
B = AttrSquare(32)
print(A.X)
A.X = 4
print(A.X)
print(B.X)