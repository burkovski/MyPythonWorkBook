trace = True

def rangetest(**arg_checks):                    # Проверяемые аргументы с диапазонами
    def err_arg(f_name, a_name, low, high):
        err_str = '{0} argument "{1}" not in {2}...{3}'
        err_msg = err_str.format(f_name, a_name, low, high)
        raise TypeError(err_msg)

    def onDecorator(func):
        if not __debug__:       # Обертывание только при отладке, иначе вернуть оригинальную ф-цию
            return func
        else:
            code = func.__code__
            all_args = code.co_varnames[:code.co_argcount]
            func_name = func.__name__

            def onCall(*args, **kwargs):
                # Все аргументы в кортеже args сопоставляются с первыми N
                # ожидаемыми аргументами по позиции
                # Остальные либо находятся в словаре kwargs, либо опущены, как
                # аргументы со значениями по умолчанию
                positionals = tuple(all_args)[:len(args)]

                for (arg_name, (low, high)) in arg_checks.items():
                    if arg_name in kwargs:
                        # Аргумент был передан по имени
                        if kwargs[arg_name] < low or kwargs[arg_name] > high:
                            err_arg(func_name, arg_name, low, high)
                    elif arg_name in positionals:
                        # Аргумент был передан по пощиции
                        pos = positionals.index(arg_name)
                        if args[pos] < low or args[pos] > high:
                            err_arg(func_name, arg_name, low, high)
                    else:
                        # Аргумент не был передан => значение по умолчанию
                        if trace:
                            print('Argument "{0}" defaulted'.format(arg_name))
                return func(*args, **kwargs)    # Тут? - ОК => вызовем оригинальную ф-цию
            return onCall
    return onDecorator

if __name__ == "__main__":
    @rangetest(age=(0, 120))
    def pers_info(name, age):
        print("{0} is {1} years old".format(name, age))

    @rangetest(m=(1, 12), d=(1, 31), y=(0, 2018))
    def birthday(m, d, y):
        print("birthday = {0}/{1}/{2}".format(m, d, y))

    pers_info("Bob", 40)
    pers_info(name="Bob", age=40)
    birthday(5, d=13, y=1963)

    class Person:
        def __init__(self, name, job, pay):
            self.name = name
            self.job = job
            self.pay = pay
        @rangetest(percent=(0.0, 1.0))
        def giveRaise(self, percent):
            self.pay += int(self.pay * percent)

    bob = Person("Bob Smith", "dev", 10000)
    sue = Person("Sue Smith", "mgr", 10000)
    bob.giveRaise(.10)
    sue.giveRaise(percent=.20)
    print(bob.pay, sue.pay)

    @rangetest(a=(1, 10), b=(1, 10), c=(1, 10), d=(1, 10))
    def omitargs(a, b=7, c=8, d=9):
        print("[a={}, b={}, c={}, d={}]".format(a, b, c, d))

    omitargs(1, 2, 3, 4)
    omitargs(1, 2, 3)
    omitargs(1, 2, 3, d=4)
    omitargs(1, d=4)
    omitargs(d=4, a=1)
    omitargs(1, b=2, d=4)
    omitargs(d=8, c=7, a=1)