"""
##############################################################################
Возвращает все имена файлов, соответствующие шаблону в дереве каталогов;
собственная версия модуля find, ныне исключенного из стандартной библиотеки:
импортируется как “PP4E.Tools.find”; похож на оригинал, но использует цикл
os.walk, не поддерживает возможность обрезания ветвей подкаталогов и может
запускаться как самостоятельный сценарий;
find() - функция-генератор, использующая функцию-генератор os.walk(),
возвращающая только имена файлов, соответствующие шаблону: чтобы получить весь
список результатов сразу, используйте функцию findlist();
##############################################################################
"""

import os
import fnmatch


def find(pattern, startdir=os.curdir):
    for(this_dir, subs_here, files_here) in os.walk(startdir):
        for name in subs_here + files_here:
            if fnmatch.fnmatch(name, pattern):
                fullpath = os.path.join(this_dir, name)
                yield fullpath


def findlist(pattern, startdir=os.curdir, dosort=False):
    matches = [find(pattern, startdir)]
    if dosort: matches.sort()
    return matches


if __name__ == '__main__':
    import sys
    namepattern, startdir = sys.argv[1], sys.argv[2]
    for name in find(namepattern, startdir):
        print(name)