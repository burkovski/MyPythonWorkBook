# Итераторы

f = open("datafile.txt")
print('\n', f.readline(), sep='', end='')  # Прочитать 4 строки из файла
print(f.readline(), end='')  # Метод readline загружает одну сроку
print(f.readline(), end='')
print(f.readline(), end='')
print(f.readline())  # Вернет пустую строку по завершении файла
f.close()

f = open("datafile.txt")  # Метод __next__ загружает одну строку
print(f.__next__(), end='')  # и возбуждает исключение StopIteration по достижении конца файла
print(f.__next__(), end='')
print(f.__next__(), end='')
print(f.__next__())
# print(f.__next__())
f.close()

for line in open("datafile.txt"):  # Использовать итератор файла: вызывает метод __next__, перехватывает исключение
    print(line.upper(), end='')  # StopIteration

f = open("datafile.txt")
print('\niter(f) is f: {}'.format(iter(f) is f))
print(next(f), end='')  # Встроеная функция next()  вызывает метод __next__
print(next(f), end='')
print(next(f), end='')
print(next(f), end='')
# print(next(f), end='')
f.close()

L = [x for x in range(1, 4)]
print("\nL = {}\niter(L) is L: {}".format(L, iter(L) is L))
I = iter(L)  # Получить объект-итератор
print(I.__next__(), end=' ')  # Вызывать __next__, чтобы перейти к следующему элементу
print(I.__next__(), end=' ')
print(next(I), end=' ')  # То же, что и вызов метода __next__
# I.__next__()
print()

print("\nIteration L = {} by for: ".format(L), end='')  # Автоматический способ выполнения итераций:
for x in L:                 # Получает итератор, вызывает __next__
    print(x, end=' ')       # Обрабатывает исключение

print("\nIteration L = {} by while: ".format(L), end='')
I = iter(L)

while True:       # Ручной способ выполнения итераций:
    try:          # Обрабатывает исключения
        x = next(I)
    except StopIteration:
        break
    print(x, end=' ')


R = range(5)            # Используется протокол итераций для обхода элементов
I = iter(R)
print("\n\nR = {}\nI = iter(R)\nnext(I): {}".format(R, next(I)))


# Генераторы

L = [1, 2, 3, 4, 5]

print("\nL = {}\nL[i] += 10 with for: ".format(L), end='')
for i in range(len(L)):         # Изменение списка в ходе итерации
    L[i] += 10
print(L)

L = [x + 10 for x in L]         # Генератор списков
print("L[i] += 10 with list generator:", L)


f = open("datafile.txt")
lines = f.readlines()
f.close()
print("\nlines = {}".format(lines))
lines = [line.rstrip() for line in lines]       # Генераторы для работы с файлами
print("lines = {}".format(lines))


X = (1, 2)
Y = (3, 4)
print("\nzip tuples: {}".format(list(zip(X, Y))))       # Упаковать кортежи
A, B = zip(*zip(X, Y))
print("unpack tuples: A = {}, B = {}".format(A, B))     # Распаковать упакованые кортежи


M = map(abs, (-1, 0, 1))
print("\nM = map(abs, (-1, 0, 1))\nM = {}".format(M))       # map возвращает итератор, а не список
print("next(M): {}".format(next(M)))                        # Непосредственное использование итратора:
print("next(M): {}".format(next(M)))                        # резкльтаты исчерпываются безвозвратно
print("next(M): {}".format(next(M)))
print("M = {}".format(list(M)))                     # Итератор map пуст: возможен только один проход
M = map(abs, (-1, 0, 1))                            # Чтобы выполнить второй проход, необходимо снова создать итератор
print("list(M): {}".format(list(M)))        # При необходимости многократного использования итератора - следует привести его к списку

