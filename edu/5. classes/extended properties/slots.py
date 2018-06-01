class limiter:
    __slots__ = ['name', 'age', 'job']  # Разешенные имена атрибутов

x = limiter()
x.name = 'Bob'  # Присваивание должно быть выплнено раньше использования
# x.pay         # Недопустимое имя: отсутствует в __slots__
print(x.name)
print()


class C:
    __slots__ = ['a', 'b']  # По умолчанию __slots__ означет отсутствие __dict__

X = C()
X.a = 1
# print(x.__dict__) # <= Ошибка
print(getattr(X, 'a'))      # Однако, функции getattr и setattr по-прежнему работают
setattr(X, 'b', 2)
print(X.b)
print('a' in dir(X))        # И dir() также отыскивает атрибуты в слотах
print('b' in dir(X))
print()


class D:
    __slots__ = ['a', 'b']
    # def __init__(self): self.d = 4    <= ошибка: невозможно добавить новый атрибут в отсутвии __dict__
X = D()


class D:
    __slots__ = ['a', 'b', '__dict__']  # Добавит __dict__ в слоты
    c = 3                               # Атрибуты класса действуют, как обычно
    def __init__(self): self.d = 4      # Имя d будет добавлено в __dict__, а не в __slots__

X = D()
print(X.d)
print(X.__dict__)   # Экземпляр имеет оба атрибута: __dict__ и __slots__
print(X.__slots__)  # getattr() может извлекать атрибуты любого типа
print(X.c)
# print(X.a)          # Все атрибуты не определены, пока им не будет присвоено значение
X.a = 1
X.b = 2
print(getattr(X, 'a'), getattr(X, 'c'), getattr(X, 'd'))
print()

for attr in list(X.__dict__) + X.__slots__:     # Учесть две формы хранения атрибутов
    print(attr, '=>', getattr(X, attr))
print()

for attr in list(getattr(X, "__dict__", [])) + getattr(X, "__slots__", []):     # Более правильный способ(значения по умолчанию)
    print(attr, '=>', getattr(X, attr))


class E:
    __slots__ = ['c', 'd']          # Суперкласс имеет слоты

class D(E):
    __slots__ = ['a', '__dict__']   # Его подкласс также имеет слоты

X = D()
X.a, X.b, X.c = 1, 2, 3             # Экземпляр объединяет слоты в себе
print(X.a, X.b)
print(E.__slots__)              # Но в классах слоты не объединяются
print(D.__slots__)
print(X.__slots__)              # Экземпляр наследует __slots__ *ближайшего* класса
print(X.__dict__)               # И имеет собственный атрибут __dict__