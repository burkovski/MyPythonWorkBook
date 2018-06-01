import time
class timer:
    def __init__(self, func):
        self.func = func
        self.all_time = 0
    def __call__(self, *args, **kwargs):
        start = time.clock()
        result = self.func(*args, **kwargs)
        elapsed = time.clock() - start
        self.all_time += elapsed
        print("{0}: {1:.5f}, {2:.5f}".format(self.func.__name__,
                                             elapsed,
                                             self.all_time))
        return result

@timer
def listComp(N):
    return [x * 2 for x in range(N)]

@timer
def mapCall(N):
    return list(map(lambda x: x * 2, range(N)))

res = listComp(5)
listComp(50000)
listComp(500000)
listComp(1000000)
print(res)
print("All time = {0}\n".format(listComp.all_time))
res = mapCall(5)
mapCall(50000)
mapCall(500000)
mapCall(1000000)
print(res)
print("All time = {0}\n".format(mapCall.all_time))
print("map/comp = {0}".format(mapCall.all_time / listComp.all_time))