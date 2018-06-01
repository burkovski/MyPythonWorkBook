import time
import sys

trace = lambda *args: None  # или print()
timefunc = time.clock if sys.platform == 'win32' else time.time

def timer(func, *args, _reps=1000, **kwargs):
    trace(func, args, kwargs, _reps)
    start = timefunc()
    for i in range(_reps):
        ret = func(*args, **kwargs)
    elapsed = timefunc() - start
    return elapsed, ret

def best(func, *args, _reps=50, **kwargs):
    best = 3 ** 32
    for i in range(_reps):
        time, ret = timer(func, *args, _reps=1, **kwargs)
        if time < best:
            best = time
    return best, ret