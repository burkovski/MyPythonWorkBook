"""
Ограиничение на чтение значений частных атрибутов экземпляров классов.
Декоратор действует как Doubler = Private('data', 'size')(Doubler).
Функция Private возвращает onDecorator, onDecorator возвращает onInstance,
а каждый экземпдяр onInstance встраивается эекзпеляр Doubler.
"""

traceMe = False
def trace(*args):
    if traceMe:
        print("[{0}]".format(' '.join(map(str, args))))

def private(*privates):
    print('private')
    def onDecorator(aClass):
        print('onDec')
        class onInstance:
            def __init__(self, *args, **kwargs):
                print('onInst')
                self.wrapped = aClass(*args, **kwargs)
            def __getattr__(self, item):
                trace('get:', item)
                if item in privates:
                    raise TypeError("private attribute fetch: " + item)
                else:
                    return getattr(self.wrapped, item)
            def __setattr__(self, key, value):
                trace("set:", key, value)
                if key == 'wrapped':
                    self.__dict__[key] = value
                elif key in privates:
                    raise TypeError("private attribute change: " + key)
                else:
                    setattr(self.wrapped, key, value)
        return onInstance
    return onDecorator

if __name__ != "__main__":
    traceMe = True

    @private('data', 'size')
    class Doubler:
        def __init__(self, label, start):
            self.label = label
            self.data = start
        def size(self):
            return len(self.data)
        def double(self):
            for i in range(len(self.data)):
                self.data[i] *= 2
        def display(self):
            print("{0} => {1}".format(self.label, self.data))

    X = Doubler("X is", [1, 2, 3])
    Y = Doubler("Y is", [-10, -20, -30])
    print(X.label)
    X.display()
    X.double()
    X.display()
    print(Y.label)
    Y.display()
    Y.double()
    Y.display()
    Y.label = "SPAM"
    Y.display()
