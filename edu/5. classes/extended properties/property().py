class NewProps:
    def getage(self):
        return 40
    def setage(self, value):
        print("set age: {0}".format(value))
        self._age = value
    age = property(getage, setage, None, None)    # get, set, del, doc

X = NewProps()
print(X.age)    # Вызовет метод getage()
X.age = 41      # Вызовет метод setage()
print(X._age)   # Нормальная операция извлечения: нет вызова getage() - _age не определяется property()
X.job = "trainer"   # Нормальная операция присваивания атрибута: нет вызова setage()
print(X.job)        # Нормальная операция извлечения атрибута: нет вызвоа getage()
print()


class Classic:
    def __getattr__(self, item):        # При обращении к неопределенным атрибутам
        if item == "age":
            return 40
        else:
            raise AttributeError
    def __setattr__(self, key, value):      # Для всех операций присваивания
        print("set {0}: {1}".format(key, value))
        if key == "age":
            self.__dict__["_age"] = value
        else:
            self.__dict__[key] = value

X = Classic()
print(X.age)    # Вызовет метод __getattr__
X.age = 41      # Вызовет метод __setattr__
print(X._age)   # Определен, нет вызова __getattr__
X.job = "trainer"   # Запустит метод __setattr__ опять
print(X.job)        # Определен: нет вызова __getattr__
