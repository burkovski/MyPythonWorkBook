class Set:
    def __init__(self, value=[]):   # Конструктор
        self.data = []              # Управляет списком
        self.concat(value)

    def intersect(self, other):     # other - любая последовательность
        res = []
        for x in self.data:         # Выбрать общие элементы
            #if x in other:
            res.append(x)
        return Set(res)             # Вернуть экземпляр

    def union(self, other):         # other - любая последовательность
        res = self.data.copy()      # Создать копию списка
        for x in other:             # Добавить элементы из other
            #if x not in res:
            res.append(x)
        return Set(res)

    def concat(self, value):
        for x in value:             # Пропустить дубликаты
            if x not in self.data:
                self.data.append(x)

    def __repr__(self):
        return "Set: {0}".format(self.data)


x = Set([1, 2, 3, 3, 4, 2])
y = x.union([3, 5, 4, 1, 6])
z = x.intersect([1, 2, 3])
print(x)
print(y)
print(z)
print(Set())