class General(Exception): pass
class Specific1(General): pass
class Specific2(General): pass

def raiser0(): raise General
def raiser1(): raise Specific1
def raiser2(): raise Specific2

for func in (raiser0, raiser1, raiser2):
    try:
        func()
    except General as X:
        print("caught:", X.__class__)   # То же, что и sys.exc_info()[0]

try:
    raise General("spam")   # Передать аргумент в конструктор => self.args = ("spam",)
except General as X:
    print(X, X.args)        # Выведет агрументы, сохараненные конструктором


import sys
class FormatError(Exception):
    def __init__(self, line, file):
        self.line = line
        self.file = file

def parser():
    raise FormatError(42, "spam.txt")  # Елси обнаружена ошибка
parser()
try:
    parser()
except FormatError as exc:
    print('Error at: file=<{0}>, line={1}'.format(exc.file, exc.line))
    for arg in sys.exc_info():
        print(arg)