def selfCheck():
    print("\n{}".format('=' * 50))
    bob = CardHolder('1234-5678', "Bob Smith", 40, '123 main st')
    print(bob.acct, bob.name, bob.age, bob.remain, bob.addr, sep=' / ')
    bob.name = "Bob Q. Smith"
    bob.age = 50
    bob.acct = "23-45-67-89"
    print(bob.acct, bob.name, bob.age, bob.remain, bob.addr, sep=' / ')

    sue = CardHolder("5678-12-34", "Sue Jones", 35, '123 main st')
    print(sue.acct, sue.name, sue.age, sue.remain, sue.addr, sep=' / ')
    try:
        sue.age = 200
    except ValueError as exc:
        print("Bad age for Sue:", exc.args[0])
    try:
        sue.remain = 5
    except:
        print("Can't set sue.remain")
    try:
        sue.acct = "1234567"
    except Exception as exc:
        print("Bad acct for Sue:", exc.args[0])
    print("{}".format('=' * 50))


class CardHolder:
    acctlen = 8         # Данные класса
    retireage = 59.5

    def __init__(self, acct, name, age, addr):
        self.acct = acct    # Данные экземпляра
        self.name = name    # Эти операции вызывают методы записи свойств
        self.age = age
        self.addr = addr    # addr - неуправляемый атрибут
                            # remain - не имеет фактических данных
    def getName(self):
        return self.__name
    def setName(self, value):
        value = value.lower().replace(' ', '_')
        self.__name = value
    name = property(getName, setName)

    def getAge(self):
        return self.__age
    def setAge(self, value):
        if value < 0 or value > 150:
            raise ValueError("invalid age")
        else:
            self.__age = value
    age = property(getAge, setAge)

    def getAcct(self):
        return self.__acct[:-3] + "***"
    def setAcct(self, value):
        value = value.replace('-', '')
        if len(value) != self.acctlen:
            raise TypeError("invalid acct number")
        else:
            self.__acct = value
    acct = property(getAcct, setAcct)

    def remainGet(self):
        return self.retireage - self.age
    remain = property(remainGet)
selfCheck()


class CardHolder:
    acctlen = 8
    retireage = 59.5

    def __init__(self, acct, name, age, addr):
        self.acct = acct
        self.name = name
        self.age = age
        self.addr = addr

    class Name:
        def __get__(self, instance, owner):
            return self.name
        def __set__(self, instance, value):
            value = value.lower().replace(' ', '_')
            self.name = value
    name = Name()

    class Age:
        def __get__(self, instance, owner):
            return self.age
        def __set__(self, instance, value):
            if value < 0 or value > 150:
                raise ValueError("invalid age")
            else:
                self.age = value
    age = Age()

    class Acct:
        def __get__(self, instance, owner):
            return self.acct[:-3] + '***'
        def __set__(self, instance, value):
            value = value.lower().replace('-', '')
            if len(value) != instance.acctlen:
                raise TypeError("invalid acct number")
            else:
                self.acct = value
    acct = Acct()

    class Remain:
        def __get__(self, instance, owner):
            return instance.retireage - instance.age    # Вызвовет Age.__get__
        def __set__(self, instance, value):
            raise TypeError("cannot set remain")
    remain = Remain()
selfCheck()


class CrdHolder:
    acctlen = 8
    retireage = 59.5

    def __init__(self, acct, name, age, addr):
        self.acct = acct
        self.name = name
        self.age = age
        self.addr = addr

    def __getattr__(self, item):
        if item == "acct":
            return self._acct[:-3] + "***"
        elif item == "remain":
            return self.retireage - self.age
        else:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        if key == "name":
            value = value.lower().replace(' ', '_')
        elif key == "age":
            if value < 0 or value > 150:
                raise ValueError("invalid age")
        elif key == "acct":
            key = "_acct"
            value = value.lower().replace('-', '')
            if len(value != self.acctlen):
                raise TypeError("invalid acct number")
        elif key == "remain":
            raise TypeError("cannot set remain")
        self.__dict__[key] = value
selfCheck()


class CardHolder:
    acctlen = 8
    retireage = 59.5

    def __init__(self, acct, name, age, addr):
        self.acct = acct
        self.name = name
        self.age = age
        self.addr = addr

    def __getattribute__(self, item):
        superget = object.__getattribute__      # Не зацикливается: на уровень выше
        if item == "acct":
            return superget(self, 'acct')[:-3] + "***"
        elif item == "remain":
            return superget(self, 'retireage') - superget(self, 'age')
        else:
            return superget(self, item)    # name, age, addr: сохраняются
    def __setattr__(self, key, value):
        if key == "name":
            value = value.lower().replace(' ', '_')
        elif key == "age":
            if value < 0 or value > 150:
                raise ValueError("invalid age")
        elif key == "acct":
            value = value.replace('-', '')
            if len(value) != self.acctlen:
                raise TypeError("invalid acct number")
        elif key == "remain":
            raise TypeError("cannot set remain")
        self.__dict__[key] = value
selfCheck()