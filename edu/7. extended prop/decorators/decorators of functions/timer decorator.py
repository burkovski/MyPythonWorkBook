import time

def timer(label='', trace=True):
    class Timer:
        def __init__(self, func):
            self.func = func
            self.all_time = 0
        def __call__(self, *args, **kwargs):
            start = time.clock()
            result = self.func(*args, **kwargs)
            elapsed = time.clock() - start
            self.all_time += elapsed
            if trace:
                format_srt = "{0} {1}: {2:.5f}, {3:.5f}"
                format_arg = (label, self.func.__name__, elapsed, self.all_time)
                format_res = format_srt.format(*format_arg)
                print(format_res)
            return result
    return Timer

if __name__ == "__main__":
    @timer(label='[CCC]==>')
    def listComp(N):
        return [x * 2 for x in range(N)]

    @timer(trace=True, label='[MMM]==>')
    def mapCall(N):
        return list(map(lambda x: x * 2, range(N)))

    for func in (listComp, mapCall):
        print()
        result = func(5)
        func(50000)
        func(500000)
        func(1000000)
        print(result)
        print("All time = {0}".format(func.all_time))
    print("map/comp = {0}".format(round(mapCall.all_time / listComp.all_time, 3)))