"""
##############################################################################
Порядок использования: python dirdiff.py dir1-path dir2-path
Сравнивает два каталога, пытаясь отыскать файлы, присутствующие в одном
и отсутствующие в другом.
Эта версия использует функцию os.listdir и выполняет поиск различий между двумя
списками. Обратите внимание, что сценарий проверяет только имена файлов, но не
их содержимое, – версию, которая сравнивает результаты вызова методов .read(),вы
найдете в сценарии diffall.py.
##############################################################################
"""

import os
import sys


def reportdiffs(unique1, unique2, dir1, dir2):
    """
    Генерирует отчет о различиях для одного каталога: часть вывода функции
    comparedirs
    """
    if not(unique1 or unique2):
        print("Directory lists are identical")
    else:
        if unique1:
            print("Files unique to:", dir1)
            for file in unique1:
                print("\t...", file)
        if unique2:
            print("Files unique to:", dir2)
            for file in unique2:
                print("\t...", file)


def difference(seq1, seq2):
    """
    Возвращает элементы, присутствующие только в seq1;
    Операция set(seq1) - set(seq2) даст аналогичный результат, но множества
    являются неупорядоченными коллекциями, поэтому порядок следования
    элементов в каталоге будет утерян
    """
    return [item for item in seq1 if item not in seq2]


def comparedirs(dir1, dir2, files1=None, files2=None):
    """
    Сравнивает содержимое каталогов, но не сравнивает содержимое файлов;
    функции listdir может потребоваться передавать аргумент типа bytes, если
    могут встречаться имена файлов, недекодируемые на других платформах
    """
    print("Comparing", dir1, "to", dir2)
    if files1 is None: files1 = os.listdir(dir1)
    if files2 is None: files2 = os.listdir(dir2)
    unique1 = difference(files1, files2)
    unique2 = difference(files2, files1)
    reportdiffs(unique1, unique2, dir1, dir2)
    return not (unique1 or unique2)             # true, если нет различий


def getargs():
    try:
        dir1, dir2 = sys.argv[1:]
    except Exception:
        print("Usage: dirdiff.py dir1 dir2")
        sys.exit(1)
    else:
        return dir1, dir2


if __name__ == '__main__':
    dir1, dir2 = getargs()
    comparedirs(dir1, dir2)
