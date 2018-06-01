def rangetest(*argchecks):          # Проверяет позиционные аргументы на вхождение
    def onDecorator(func):          # в заданый диапазон
        if not __debug__:           # True - если "python -0 main.py args..."
            return func             # Ничего не выполняет: просто возвращает
        else:                       # оригинальную функцию
            def onCall(*args):      # Иначе, на этапе отладки, возвращает обертку
                for(ix, low, high) in argchecks:
                    if args[ix] < low or args[ix] > high:
                        errmsg = "Arguments {0} not in {1}...{2}".format(ix, low, high)
                        raise TypeError(errmsg)
                return func(*args)
            return onCall
    return onDecorator


if __name__ == "__main__":
    print(__debug__)

    @rangetest((1, 0, 120))     # Значение age должно быть в диапазоне 0...120
    def persinfo(name, age):    # persinfo = rangetest(...)(persinfo)
        print("{0} is {1} years old".format(name, age))
    persinfo = rangetest(persinfo)

    @rangetest([0, 1, 12], [1, 1, 31], [2, 0, 2009])
    def birthday(m, d, y):
        print("Birthday: {0}/{1}/{2}".format(m, d, y))

    class Person:
        def __init__(self, name, job, pay):
            self.name = name
            self.job = job
            self.pay = pay
        @rangetest([1, 0.0, 1.0])           # give_raise = rangetest(...)(give_raise)
        def give_raise(self, percent):      # Аргумент 0 - ссылка self на экземпляр
            self.pay += int(self.pay * percent)

    persinfo("Bob Smith", 50)                   # onCall(...)
    birthday(5, 31, 1963)
    sue = Person("Sue Jones", "dev", 100000)
    sue.give_raise(0.10)                        # onCall(self, 0.10)
    print(sue.pay)