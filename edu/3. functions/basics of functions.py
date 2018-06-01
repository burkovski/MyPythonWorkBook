def times(x, y):  # Создать функцию и связать ее с именем
    return x * y  # Тело, выполняемое при вызове функции


print(times(2, 4))  # Вызов функции
print(times("Hi!", 4))
print()


def intersect1(seq1, seq2):
    res = []
    for x in seq1:
        if x in seq2:
            res.append(x)
    return res


print(intersect1("SPAM", "SCAM"))
print()


def intersect2(seq1, seq2):
    return [x for x in seq1 if x in seq2]   # Более быстрый вариант


print(intersect2("SPAM", "SCAM"))
print(intersect2([1, 2, 3], (1, 4)))    # Смешивание типов
