from math import sqrt
from mylib import mytimer

# EX 2
# def adder(first, second):
#     return first + second
#
# print(adder(1, 2))
# print(adder("sp", "am"))
# print(adder([1, 2], [3, 4]))


# EX 3
# def adder(*args):
#     sum, *rest = args
#     for x in rest:
#         sum += x
#     return sum
#
# print(adder(1, 2, 3, 4))
# print(adder(1))
# print(adder('qwe', 'r', 'ty'))
# print(adder([1, 2], [3, 4], [5]))


# EX 4
# def adder(**kwargs):
#     sum, *rest = list(kwargs.values())
#     for x in rest:
#         sum += x
#     return sum
#
# print(adder(a=3, b=4, c=5))
# print(adder(f='qwe', s='r', th='ty'))


# EX 5
# def copy_dict(old_dict):
#     return {key: value for (key, value) in old_dict.items()}
#
# D = {'a': 1, 'b': 2, 'c': 3}
# D1 = copy_dict(D)
# print(D1)
# print(D is D1)


# EX 6
# def add_dicts(dict1, dict2):
#     new_dict = {key: value for (key, value) in dict1.items()}
#     new_dict.update({key: value for (key, value) in dict2.items()})
#     return new_dict
#
# print(add_dicts({'a': 1, 'b': 2, 'c': 3}, {'d': 4}))


# EX 9
# L = [1, 4, 9, 16, 25]
#
# def for_loop(L):
#     res = []
#     for x in L:
#         res.append(sqrt(x))
#     return res
#
# def map_call(L):
#     return list(map(sqrt, L))
#
# def list_gen(L):
#     return [sqrt(x) for x in L]
#
# print(for_loop(L))
# print(map_call(L))
# print(list_gen(L))


# EX 10
reps = 10000
replist = range(reps)

def math_mod():
    for i in replist:
        res = sqrt(i)
    return res

def pow_call():
    for i in replist:
        res = pow(i, .5)
    return res

def pow_expr():
    for i in replist:
        res = i ** .5
    return res

for tester in (mytimer.best, mytimer.timer):
    print("\n<%s>" % tester.__name__)
    for test in (math_mod, pow_call, pow_expr):
        elapsed, result = tester(test)
        print('-' * 42)
        print("%-9s: %5f => %s" % (test.__name__, elapsed, result))