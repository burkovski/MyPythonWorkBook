choice = "eggs"
switch = {"spam": 1.25,
          "ham": 1.99,          # Использование структуры множественного ветвления
          "eggs": 0.99,         # switch на базе словаря
          "bacon": 1.10}
print("\nSwitch statement:", switch.get("eggs", "Bad choice!"), '\n')


# Проверка истинности:
print(2 or 3, 3 or 2, [] or 3, [] or {})         # Вернет левый операнд, если он имеет истинное значение, иначе - вернет правый операнд(Истинный или ложный)
print(2 and 3, 3 and 2, [] and 3, [] and {}, '\n')     # Вернет левый операнд, если он имеет ложное значение, иначе - вернет правый операнд(Истинный или ложный)


X = 1
Y = 2
Z = 3

if X:
    A = Y               # Трехместное выражение if/else
else:
    A = Z
print(A)

A = Y if X else Z       # Альтернативная конструкция
print(A)

A = ((X and Y) or Z)    # Тот же результат, при помощи логических проверок
print(A)