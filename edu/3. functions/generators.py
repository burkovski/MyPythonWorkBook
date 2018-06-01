s = "spam"
res1 = list(map(ord, s))    # Применить функцию к последовательности
res2 = [ord(x) for x in s]  # Применить выражение к последовательности
print("\ns = {}\nres1 = list(map(ord, s)): {}\nres2 = [ord(x) for x in s]: {}\n".format(s, res1, res2))

seq = list(range(10))
res1 = list(map(lambda x: x ** 2, seq))
res2 = [x ** 2 for x in seq]
print(("seq = {}\nres1 = list(map(lambda x: x ** 2, seq)): {}\n"
       "res2 = [x ** 2 for x in seq]: {}\n").format(seq, res1, res2))


res1 = list(filter(lambda x: x % 2 == 0, seq))
res2 = [x for x in seq if x % 2 == 0]
print(("seq = {}\nres1 = list(map(lambda x: x ** 2, seq)): {}\n"
       "res2 = [x for x in seq if x % 2 == 0]: {}\n").format(seq, res1, res2))


res1 = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, seq)))
res2 = [x ** 2 for x in seq if x % 2 == 0]
print(("seq = {}\nres1 = list(filter(lambda x: x % 2 == 0, seq)): {}\n"
       "res2 = [x ** 2 for x in seq if x % 2 == 0]: {}\n").format(seq, res1, res2))


def gensquares(seq):
    for i in seq:
        yield i ** 2    # Позднее продолжить работу с этого места

res = list(gensquares(seq))
res1 = list(map(lambda x: x ** 2, seq))
res2 = [x ** 2 for x in seq]

print(("seq = {}\nres = list(gensquares(seq)): {}\n"
       "res1 = list(map(lambda x: x ** 2, seq)): {}\n"
       "res2 = [x ** 2 for x in seq]: {}\n").format(seq, res, res1, res2))

S = "spam"

def timeout(s):         # Функция-генераор
    for x in s:
        yield x * 4

G1 = timeout(s)
G2 = (x * 4 for x in S)    # Выражение-генератор

print("S = {}\n"
      "G1 = timeout(S): {}\nlist(G1): {}\n"     # Принудительно получить все результаты вызовом list()
      "G2 = (x * 4 for x in S): {}\nlist(G2): {}".format(S, G1, list(G1), G2, list(G2)))

print("\nseq = {}".format(seq))
print("[x ** 2 for x in seq] = {}".format([x ** 2 for x in seq]))           # Генератор списков: конструирует список
print("list(x ** 2 for x in seq) = {}".format(list(x ** 2 for x in seq)))   # Выражение - генератор: воспроизводит элем.
print("{x ** 2 for x in seq} = %s" % {x ** 2 for x in seq})                 # Генератор множеств
print("{{x: x ** 2 for x in seq}} = %s" % {x: x ** 2 for x in seq})         # Генератор словрей


