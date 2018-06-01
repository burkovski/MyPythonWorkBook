D = {"spam": 2, "eggs": 1, "ham": 2}    # Традиционное литеральное выражение(удобно, если заранее известно содержимое)
print(D)
print(D["spam"])
D1 = vars().copy()

for key in D1:
    print("Key: " + str(key), "Value: " + str(D1[key]), sep='\n', end='\n\n')

print(len(D))
print("__file__" in D1)
print(list(D.keys()))
D["ham"] = ["grill", "bake", "fry"]
print(D)
del D["ham"]
print(D)
D["brunch"] = "Bacon"
print(D)
print(list(D.values()))
print(list(D.items()))

print(D.get("spam"))
print(D.get("toast"))
print(D.get("toast", 88))
D2 = dict(toast=4, muffin=5)    # Форма именованых аргументов(все ключи обязательно - сторки)
D.update(D2)
print(D)
D.pop("brunch")


table = {"Python": "Guido van Rossum",
         "Perl": "Larry Wall",
         "Tcl": "John Ousterhout"}
language = "Python"
creator = table[language]
print(creator)

for lang in table:
    print(lang, '\t', table[lang])

D3 = dict([("name", "Bob"), ("age", 42)])   # Кортежи: (ключ, значение), удобно, когда содержимое хранится в последов.
print(D3)

D4 = dict.fromkeys(['a', 'b', 'c'], 0)    # Удобно использовать, если все значения одниаковые
print(D4)

print(dict(zip(['a', 'b', 'c'], [1, 2, 3])))    # Генерация словаря из результата вызова zip()
print({key: value for (key, value) in zip(['a', 'b', 'c'], [1, 2, 3])})    # Генератор словарей
print({x: x ** 2 for x in range(1, 5)})
print({c: c * 4 for c in "SPAM"})
print({c.lower(): c + '!' for c in ("SPAM", "EGGS", "HAM")})


D = {k: v for (k, v) in zip(['a', 'b', 'c'], range(1, 4))}
print(D)
K = D.keys()    # Создает объект представления
print(K)
print(list(K)[0])    # Индексация возможна только при возведении в список или любую другую последовательность
V = D.values()
print(V)
print(list(V)[0])
print(list(D.items()))

for k in D.keys(): print(k)    # Эквивалентны
for k in D: print(k)

print(list(K))
print(list(V))
D.pop('b')          # Изменения в словарях динамически отражаются в объектах отображения
print(list(K))
print(list(V))

print(K | {'x'})
print(K & {'c'})

keys = list(D.keys())
keys.sort()
for key in keys: print(key, D[key])         # Сортировка словаря

for key in sorted(D): print(key, D[key])

print(sorted(D3) < sorted(D2))