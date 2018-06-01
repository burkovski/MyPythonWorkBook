import sys


# Присваивание последовательностей:

nudge = 1
wink = 2
A, B = nudge, wink                              # Присавивание кортежей, что равносильно A = nudge; B = wink
print("\n'A' value:", A, "\n'B' value:", B)
[C, D] = [nudge, wink]                          # Присваивание списков - аналогично кортежам
print("\n'C' value:", C, "\n'D' value:", D)

print("\nBefore assignment:\nnudge:", nudge, "\nwink: ", wink)
nudge, wink = wink, nudge                                          # Благодаря присваиванию кортежей,
print("After assignment:\nnudge:", nudge, "\nwink: ", wink)        # возможен обмен значений, без временной переменной


[a, b, c] = (1, 2, 3)       # Кортеж значений присваивается списку переменных
print("\n[a, b, c] = (1, 2, 3)")
print("a:", a)
print("b:", b)

string = "SPAM"
a, b, c, d = string             # Слева и справа - одинаковое количество элементов
print("\na, b, c, d = 'SPAM'")
print("a:", a)
print("d:", d)

a, b, c = range(3)              # Присваивание последовательности целых чисел
print("\na, b, c = range(3)")
print("a:", a, "\nc:", c)


L = [val for val in range(6)]
print("\nL = {}".format(L))
while L:
    front, *L = L                                       # Получить первый и остальные элементы
    print("front: {0}, rest: {1}".format(front, L))
print()


# Инструкция print():

x = "spam"
y = 99
z = ['eggs']
print("Named args: ", x, y, z, sep='...', end='!\n')                             # Несколько именованных аргументов
print("Reversed named args: ", x, y, z, end='!\n', sep='...')                    # Порядок значения не имеет
print("printfile.txt: ", x, y, z, sep="...", end="!\n", file=open("printfile.txt", 'w'))    # Перенаправление потока вывода в файл
print(open("printfile.txt", 'r').read())


sys.stdout.write("It's output without print()!\n")   # Вывод без функции print(), посредсвтом явной записи в sys.stdout
                                                     # точный эквивалент print("It's output without print()!")


temp = sys.stdout                      # Сохранить для последующего восстановления
sys.stdout = open("log.txt", 'w')      # Перенаправить вывод в файл
print("spam")                          # Выведет в файл, а не на экран
print(1, 2, 3)
sys.stdout.close()      # Вытолкнуть буферы на диск
sys.stdout = temp       # Восттановить первоначальный поток
del temp
print("\nback here!")
print("\nRead from log.txt:", open("log.txt").read(), sep='\n')     # Прочитать содержимое log.txt

log = open("log.txt", 'w')      # Однако, удобнее использовать именованный аргумент file функции print():
print('spam', file=log)
print(1, 2, 3, file=log)
log.close()
print(open("log.txt").read())


print("Bad!" * 8, file=sys.stderr)      # Перенаправление в стандартный поток вывода


print(3 or 2, 2 or 3)

