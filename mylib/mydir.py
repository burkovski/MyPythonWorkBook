"""
mydir.py: выводит содержимое других модулей
"""

sepchar = '-'
seplen = 65

def listing(module, *, verbose=True):
    sepline = sepchar * seplen
    if verbose:
        print(sepline)
        print("name:", module.__name__, "file:", module.__file__)
        print(sepline)

    count = 1
    for attr in module.__dict__:    # Сканировать пространство имен модуля
        print("{0:02}) {1}".format(count, attr), end=' ')
        if attr.startswith('__'):
            print("<built-in name>")    # Пропустить встроеную область видимости
        else:
            print(getattr(module, attr))  # То же, что и module.__dict__[attr], module.attr и sys.modules['module'].attr
        count += 1

    if verbose:
        print(sepline)
        print(module.__name__, "has {0} names".format(count))


if __name__ == '__main__':
    listing(mydir)

