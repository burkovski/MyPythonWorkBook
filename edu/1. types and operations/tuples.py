print((1, 2) + (3, 4))    # Кортежи поддерживают конкатенацию
print((1,) * 5)           # и повторение, подобно спискам и строкам

T = (1, 2, 3, 4)                              # Кортежи являються последовательностями - им свойственны операции
print("\nT[0]:", T[1], "\nT[:-1]", T[:-1])    # индексирования и извлечения срезов

T = ("somestring",)     # Создание кортежа, состоящего из одного элемента


T = ('cc', 'aa', 'dd', 'bb')
print("\nUnsorted tuple:\t\t\t\t\t", T)
tmp = list(T)                               # Сортировка кортежа, приведением к списку
tmp.sort()
T = tuple(tmp)
print("Sorted tuple by list method:\t", T)

T = ('cc', 'aa', 'dd', 'bb')                # Сортировка, с использованием функции sorted()
T = tuple(sorted(T))
print("Sorted tuple by sorted() func:\t", T)


T = tuple(val for val in range(97, 103))
L = [chr(sm) for sm in T]
print("\n")                                         # Сборка списка из кортежа, с использованием конструктора списков
for i in range(len(T)):
    print("Code of sumbol: ", T[i], "\nSumbol:", L[i])


T = tuple("somestring")
print("\n\nTuple:", T)                                                            # Кортежи имеют только два метода:
print("Number of 's' in tuple:", T.count('s'))                                    # количество элементов в кортеже
print("Index of second 's' in tuple:", T[T.index('s') + 1:].index('s') + 1)       # индекс элемента


T = ("spam", [66, 99], 3.14)            # Кортежи гетерогенны(могут хранить объекты различных типов)
print("Old tuple:", T)                  # и поддерживают произвольное количество уровней вложенности
T[1][0], T[1][1] = T[1][1], T[1][0]     # Кроме того, изменяемые объекты внутри кортежей поддерживают изменение
print("New tuple:", T)


