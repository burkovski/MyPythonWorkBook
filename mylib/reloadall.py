"""
reloadall.py: транзитивная перезагрузка модулей
"""

import types
from importlib import reload


def status(module):
    print("reloading <{0}>".format(module.__name__))


def transitive_reload(module, visited):
    if module not in visited:  # Пропустить повторные значения
        status(module)
        reload(module)
        visited.add(module)
        for attrobj in module.__dict__.values():  # Для всех атрибутов
            if type(attrobj) == types.ModuleType:  # Рекурсия, если модуль
                transitive_reload(attrobj, visited)


def reload_all(*args):
    visited = set()
    for arg in args:
        if type(arg) == types.ModuleType:
            transitive_reload(arg, visited)


if __name__ == "__main__":
    reload_all(reloadall)