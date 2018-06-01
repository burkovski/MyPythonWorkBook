class Set(list):  # Подкласс встроеного типа list
    def __init__(self, value=None):  # Конструктор
        list.__init__(self, [])  # Адаптировать список
        if value is None:
            value = []
        self.concat(value)  # Копировать изменяемый аргумент по умолчанию

    def intersect(self, other):
        res = []
        for x in self:
            if x in other:
                res.append(x)
        return Set(res)

    def union(self, other):
        res = self.copy()
        for x in other:
            if x not in res:
                res.append(x)
        return Set(res)

    def concat(self, value):
        for x in value:
            if x not in self:
                self.append(x)

    def __repr__(self):
        return "Set: " + list.__repr__(self)

    def __and__(self, other):
        return self.intersect(other)

    def __or__(self, other):
        return self.union(other)

X = Set([1, 2, 3, 1, 3, 4])
X = X & [1, 2]
X = X | [1, 2, 3, 4, 5]
print(X.__class__, type(X))
print(Set.__class__, type(Set))
print(list.__class__, [].__class__)
