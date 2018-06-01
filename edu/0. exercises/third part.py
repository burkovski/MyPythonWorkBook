# EX 1.a
# for char in input("Enter your string!\n=> "):
#     print("Character: {}  <->  ASCII code: {}".format(char, ord(char)))
#


# EX 1.b
# total = 0
# for char in input("\nEnter your string!\n=> "):
#     print("Character: {}  <->  ASCII code: {}".format(char, ord(char)))
#     total += ord(char)
# print("Total sum of ASCII codes:", total)


# EX 1.c
# res = []
# for char in input("\nEnter your string!\n=> "):
#     res.append(ord(char))
# print("ASCII list codes:", res)


# EX 2
# for i in range(1, 51):
#     print("Hello {}\a\n".format(i))


# EX 3
# D = dict(a=3, c=8, d=46, t=6, spam=88, z=69)
# print("Dictionary:", D)
# for key in sorted(D):
#     print("Key = {} \t<->\t  Value = {}".format(key, D[key]))


# EX 4.a
# L = [1, 2, 4, 8, 16, 32, 64]
# X = 5
# i = 0
# while i < len(L):
#     if 2 ** X == L[i]:
#         print("Was found at index:", i)
#         break
#     i += 1
# else:
#     print(X, "not found")


# EX 4.b
# L = [1, 2, 4, 8, 16, 32, 64]
# X = 5
# for val in L:
#     if 2 ** X == val:
#         print("Was found at index:", L.index(val))
#         break
# else:
#     print(X, "not found")


# EX 4.c
# L = [1, 2, 4, 8, 16, 32, 64]
# X = 5
# if 2 ** X in L:
#     print("Was found at index:", L.index(2 ** X))
# else:
#     print(X, "not found")


# EX 4.d
# L = [2 ** X for X in range(7)]
# X = 5
# if 2 ** X in L:
#     print("Was found at index:", L.index(2 ** X))
# else:
#     print(X, "not found")


# EX 4.e
# L = [2 ** X for X in range(7)]
# X = 2 ** 5
# if X in L:
#     print("Was found at index:", L.index(X))
# else:
#     print(X, "not found")


