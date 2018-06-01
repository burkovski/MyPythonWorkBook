class Wrapped:
    def __init__(self, object):
        self.wrapped = object       # Сохранить объект
    def __getattr__(self, attrname):
        print("Trace:", attrname)   # Отметить факт извлечения
        return getattr(self.wrapped, attrname)  # Делегировать извлечния

if __name__ == "__main__":
    x = Wrapped([1, 2, 3])  # Обернуть список
    x.append(3)             # Делериговать операцию метода списка
    print(x.wrapped)
    x = Wrapped({'a': 1, 'b': 2})   # Обернуть словарь
    print(list(x.keys()))           # Деленировать операцию метода словаря