from mylib.classtools import AttrDisplay


class Person(AttrDisplay):
    def __init__(self, name, job=None, pay=0):      # Заполнить поля объектов при создании
        self.name = name
        self.job = job
        self.pay = pay

    def last_name(self):                # Возвращает фамилию
        return self.name.split()[-1]

    def give_raise(self, percent):      # Надбавка
        self.pay = int(self.pay * (1 + percent))


class Manager(Person):      # Подкласс класса Person
    def __init__(self, name, pay):
        Person.__init__(self, name, 'mgr', pay)   # Вывзов оригинального конструктора со значением job = 'mgr'

    def give_raise(self, percent, bonus=0.1):   # Переопределить метод для адаптации
        Person.give_raise(self, percent + bonus)    # Дополнить оригинальный метод начисления з/п



if __name__ == "__main__":              # Тестирование класса
    bob = Person("Bob Smith")           # Запуск __init__ произойдет автоматически
    sue = Person("Sue Jones", job="dev", pay=100000)

    print(bob.name, bob.pay)        # Извлечем атрибуты
    print(sue.name, sue.pay)        # Атрибуты в объектах sue и bob имеют разные прстрансва имен -> разные значения
    print(bob.last_name(), sue.last_name())
    sue.give_raise(0.1)     # Надбвака к зарплате 10%
    print(sue.pay)
    print(sue)
    print(bob)
    tom = Manager("Tom Jones", 50000)   # Указывать должность не требуется - устанавливается(подразумевается) классом
    tom.give_raise(0.1)         # Вызов адаптированой версии
    print(tom.last_name())      # Вызов уначледованого метода
    print(tom)                  # Вызов уначледованого __str__


    print(bob.__class__)             # Выведет класс объекта bob
    print(bob.__class__.__name__)    # И имя класса
    print(list(bob.__dict__.keys()))    # Атрибуты - это ключи словаря
    for key in bob.__dict__:
        print(key, '=>', bob.__dict__[key])     # Обращение по ключам
    for attr in bob.__dict__:
        print(attr, '=>', getattr(bob, attr))   # Аналогично выражению object.attribute