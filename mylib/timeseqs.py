import sys
from mylib import mytimer

reps = 10000
replist = range(reps)

def for_loop():
    res = []
    for x in replist:
        res.append(x + 1)
    return res

def list_comp():
    return [x + 1 for x in replist]

def map_call():
    return list(map(lambda x: x + 1, replist))

def gen_expr():
    return list(x + 1 for x in replist)

def gen_func():
    def gen():
        for x in replist:
            yield x + 1
    return list(gen())


if __name__ == '__main__':
    print(sys.version)
    for test in (for_loop, list_comp, map_call, gen_expr, gen_func):
        elapsed, result = mytimer.timer(test)
        print('-' * 34)
        print("%-9s: %.5f => [%s...%s]" % (test.__name__, elapsed, result[0], result[-1]))
