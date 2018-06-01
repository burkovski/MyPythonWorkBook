import time


def tracer(func):
    calls = 0
    def onCall(*args, **kwargs):
        nonlocal calls
        calls += 1
        print("call {0} to {1}".format(calls, func.__name__))
        return func(*args, **kwargs)
    return onCall


def timer(label="", trace=True):
    def onDecorator(func):
        def onCall(*args, **kwargs):
            start = time.clock()
            result = func(*args, **kwargs)
            elapsed = time.clock() - start
            onCall.all_time += 1
            if trace:
                frmt_str = "{0}{1}: {2:.5f}, {3:.5f}"
                frmt_arg = (label, func.__name__, elapsed, onCall.all_time)
                print(frmt_str.format(*frmt_arg))
            return result
        onCall.all_time = 0
        return onCall
    return onDecorator