class FirstClass:               # Определяет объект класса
    def setdata(self, value):   # Определяет метод класса
        self.data = value       # self - это экземпляр класса
    def display(self):
        print(self.data)        # self.data: данные экземпляров

x = FirstClass()        # Создаются два экземпляра
y = FirstClass()        # Каждый является отдельным пространством имен

x.setdata("King Artur")     # Вызов метода: self - это x
y.setdata(3.1415)           # Эквивалентно: FirstClass.setdata(y, 3.1415)

x.display()     # В каждом экземпляре свое значение self.data
y.display()

x.data = "New value"    # Можно получать/записывать значения атрибутов за пределами класса
x.display()


class SecondClass(FirstClass):  # Наследует setdata
    def display(self):          # Переопределяет display
        print("Current value =", self.data)

z = SecondClass()
z.setdata(42)       # Найдет метод setdata в FirstClass
z.display()         # Найдет переопределенный метод в SecondClass


class ThirdClass(SecondClass):  # Наследует SecondClass
    def __init__(self, value):  # Вызывается при создании экземпляра выражением ThirdClass(value)
        self.data = value
    def __add__(self, other):   # Для выражения self + other
        return ThirdClass(self.data + other)
    def __str__(self):          # Вызывается из print(self), str()
        return "[ThirdClass: {0}]".format(self.data)
    def mul(self, other):       # Обычный метод класса
        self.data *= other

a = ThirdClass("abc")   # Вызовет __init__
a.display()             # Унаследованый метод
print(a)                # __str__: возвращает строку
b = a + 'xyz'           # Новый метод __add__: создается новый экземпляр класса
print(b)                # __str__: возвращает строку
a.mul(3)                # mul: изменяется сам экземпляр
print(a)