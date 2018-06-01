L = []
print(L)
L.append(1)
print(L)
L.extend([2, 3, 4, 5, 7, 6, 9, 8])
print(L)

L = list("spam")
print(L)
L = list(range(-5, 6, 2))
print(L)
L[2:4] = [1, 0, -1]
print(L)
L = L + [32, 23, 2, 3]
print(L)
L1 = [0] * len(L)
print(L1, 0 in L1)


L.insert(4, 1)
print(L)
print(L.index(32))
print(L.count(1))
L.sort()
print(L)
del L[L.index(1)]
del L[5:len(L)]
print(L)
L.reverse()
print(L)
L.pop()
print(L)
L.remove(L[-1])
print(L)
L2 = [x for x in range(0, 21) if x % 2 == 0]
print(L2)
L3 = list(map(ord, "somestring"))
print(L3)
