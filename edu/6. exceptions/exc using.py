# В нескольких функциях
def action2():
    print(1 + [])       # Возбуждает исключение TypeError

def action1():
    try:
        action2()
    except TypeError:   # Самая последняя соотвествующая инструкция try
        print("inner try")

try:
    action1()
except TypeError:       # Этот обработчик будет вызван, только если
    print("outer try")  # action1 повтороно возбудит исключение


# Вложенные инструкции
try:
    try:
        action2()
    except TypeError:       # Самая последняя соотвествующая инструкция try
        print("inner try")
except TypeError:           # Этот обработчик будет вызван, только если
    print("outer try")      # вложеный обработчик повторно возбудит исключение


def raise1(): raise IndexError
def nonraise(): return
def raise2(): return # raise SyntaxError

for func in (raise1, nonraise, raise2):
    print("\n{0}".format(func))
    try:
        try:
            func()
        except IndexError:
            print("caught IndexError")
    finally:
        print("finally run")


print()
class Failure(Exception):
    pass

def searcher(x):    # Поиск элемента
    if x in [1, 2, 3, 4, 5]:    # Если элемент найден
        return x    # Вернем значение
    else:    # Если не нашлось
        raise Failure    # Возбудим исключение, как флаг неудачного поиска

x = 3
try:
    searched_elem = searcher(x)
except Failure:     # Если поиск не увенчался успехом
    print("Element {0} not found!".format(x))    # Обработка неудачного поиска
else:       # Обработка найденного элемента
    print("Done!")
