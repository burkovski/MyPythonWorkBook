X = 99      # X и func определены в модуле: глобальная область

def func(Y):    # Z и Y определены в функции: локальная область
    # Локльная область вилимости
    Z = X + Y   # X - глобальная переменная
    return Z

print("X =", func(1))  # func в модуле: вернет число 100


def f1():           # X - имя в глобальной видимости
    X = 88          # Локальное имя в объемлющей функции
    def f2():
        print("\nX =", X)    # Обращение к переменной во вложеной функции
    f2()

f1()                # Выведет 88: локальная переменная в объемлющей функции


def f1():
    x = 88
    def f2():
        print("\nX =", x)      # Сохраняет значение Х в объемлющей области видимости
    return f2         # Возвращает f2, но не вызывает ее

action = f1()       # Создает и возвращает функцию
action()            # Вызов этой функции выведет 88


def maker(n):
    def action(x):          # Создать и вернуть функцию
        return x ** n       # Функция action запоминает занечение N в объемлющей области видимости
    return action

f = maker(2)                    # Запишет 2 в N
print("\n3 ** 2 =", f(3))       # Запишет 3 в Х, но в N - по прежнему 2
g = maker(3)                    # Функция g хранит число 3, а f - число 2
print("3 ** 3 =", g(3))         # 3 ** 3 = 27
print("3 ** 2 =", f(3))         # 3 ** 2 = 9; f по прежнему хранит в N число 2


def f1():
    x = 88
    def f2(x=x):            # Сохранит значение Х в объемлющей области в виде аргумента
        print("\nX =", x)
    f2()
f1()                        # Выведет 88


def f1():
    x = 88
    f2(x)     # Передача значения Х, вместо вложения функций; опережающие ссылки считаются допустимыми

def f2(x):
    print("\nX =", x)

f1()


def f1():
    x = 4
    action = (lambda n: x ** n)     # Запоминается Х из объемлющей инструкции def
    return action

x = f1()
print("\n4 ** 2 =", x(2))


def makeActions():
    acts = []
    for i in range(5):                  # Сохранить каждое значение i
        acts.append(lambda x: x * i)    # Все запомнят последнее значение i!
    return acts

acts = makeActions()
print("\nacts[1](2) =", acts[1](2))       # Вернет 4 * 2, должно - 1 * 2
print("acts[4](2) =", acts[4](2))


def makeActions():
    acts = []
    for i in range(5):                       # Использовать значение по умолчанию
        acts.append(lambda x, i=i: x * i)    # Сохранить текущее значение i!
    return acts

acts = makeActions()
print("\nacts[1](2) =", acts[1](2))          # Заработало!
print("acts[4](2) =", acts[4](2), '\n')



def tester(start):
    state = start               # Обращение к нелокальным переменным
    def nested(label):          # действует как обычно
        print(label, state)     # Извлекает значение state из области видимости
    return nested               # объемлющей функции

F = tester(0)
F("Spam!")
F("Ham!")
print()


def tester(start=0):
    state = start
    def nested(label):
        nonlocal state          # Объект state находится в объемлющей области видимости
        print(label, state)
        state += 1              # Изменит значение переменной, объявленой как nonlocal
    return nested

F = tester(0)
F("Spam!")          # Значение state будет увеличиваться при каждом вызове
F("Ham!")
F("Eggs!")
print()


class tester():                     # Альтернативное решение на основе классов
    def __init__(self, start):      # Коструктор объекта
        self.state = start          # сохранение информации о новом объекта
    def nested(self, label):
        print(label, self.state)    # Явное обращение к информации
        self.state += 1             # Изменения всегда допустимы

F = tester(0)           # Создаст экзаплемпляр класса, вызовет  __init__
F.nested("Spam!")       # Ссылка на F будет передана в аргументе self
F.nested("Ham!")

G = tester(42)          # Каждый экземпляр получает свою копию информации
G.nested("Toast!")      # Изменения в одном объекте не сказываются на других
G.nested("Bacon!")
F.nested("Tomato!")     # В объекте F сохранилась прежняя информация
F.nested("Eggs!")
print("F.state =", F.state, '\n')   # Информация может быть получена за пределами класса


class tester():
    def __init__(self, start):
        self.state = start
    def __call__(self, label):          # Вызывается при вызове экхемпляра
        print(label, self.state)        # Благодаря ему отпадает
        self.state += 1                 # неопходимость в методе .nested()

H = tester(99)
H("Juice!")         # Вызывает метод __call__
H("Pancakes!")
print()


def tester(start):
    def nested(label):
        print(label, nested.state)
        nested.state += 1           # Изменит атрибут, а не значение имени nested
    nested.state = start            # Инициализация после создания функции
    return nested

F = tester(0)
F("Spam!")      # F - это функция 'nested' с присоединенным атрибутом state
F("Ham!")
print("F.state =", F.state)     # Атрибут state доступен за пределами функции
G = tester(42)
G("Eggs!")          # G имеет собственный атрибут state, отличный от F
F("Bread!")