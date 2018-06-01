print()
x = "spam"
while x:    # Пока Х - не пустая строка
    print(x, end=' ')
    x = x[1:]   # Вырезать из Х первый элемент

print()
# while True:
#     name = input("\nEnter the name: ")
#     if name == "stop": break
#     age = int(input("Enter the age: "))
#     print("Hello, {} => {}".format(name, age ** 2))


# for i in input("Enter the string: "):      # Обход строки
#    print(i, end=' ')
# print()


print()
T = [(1, 2), (3, 4), (5, 6)]
for (a, b) in T:                # Операция присваивания кортежа в действии
    print(a, b)


print()
D = {'a': 1, 'b': 2, 'c': 3}
for key in D:                               # Используется итератор словаря и индексировние
    print("{} => {}".format(key, D[key]))

print()
for (key, value) in D.items():              # Обход ключей и значений одноверменно
    print("{} => {}".format(key, value))

print()
seq1 = "spam"
seq2 = "scam"

res = []                    # Изначально список пуст
for x in seq1:              # Выполнить обход последовательности
    if x in seq2:           # Общий элемент?
        res.append(x)       # Добавить результат в список
print(', '. join(res))



X = "SPAM"

print()
for item in X:              # Простейший цикл
    print(item, end=' ')

print()
i = 0
while i < len(X):           # Обход с помощью while
    print(X[i], end=' ')
    i += 1

print()
for i in range(len(X)):     # Извлечение элементов вручную
    print(X[i], end=' ')
print()


S = "qwertytrewq"

print()
for i in range(0, len(S), 2):       # Создание индексов функцией range()
    print(S[i], end=' ')

print()                             # Создание среза - лучший способ
for item in S[::2]:
    print(item, end=' ')


L1 = [1, 2, 3, 4]
L2 = [5, 6, 7, 8]
print("\n\nL1 = [1, 2, 3, 4]\nL2 = [5, 6, 7, 8]\nWith zip() iter:")
for (x, y) in zip(L1, L2):
    print("{} + {} = {}".format(x, y, x + y))


D1 = {"spam": 1, "eggs": 2, "ham": 3}
print("\nD1:", D1)
D2 = {}
values = D1.values()
keys = D1.keys()

for (k, v) in zip(keys, values):        # Конструирование словаря с помощью zip() и for
    D2[k] = v
print("D2:", D2)


print("\nX = 'SPAM'\nenumerate(X):")
for (offset, item) in enumerate(X):
    print(item, "arrears at offset", offset)