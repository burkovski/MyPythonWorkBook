"""
##############################################################################
Порядок использования: “python ...\Tools\search_all.py dir string”.
Отыскивает все файлы в указанном дереве каталогов, содержащие заданную строку;
для предварительного отбора имен файлов использует интерфейс os.walk вместо
find.find; вызывает visitfile для каждой строки в результатах, полученных
вызовом функции find.find с шаблоном “*”;
##############################################################################
"""

import os
import sys

listonly = False
textexts = ['.py', '.pyw', '.txt', '.c', '.h']


def searcher(startdir, searchkey):
    global fcount, vcount
    fcount = vcount = 0
    for (thisdir, dirshere, fileshere) in os.walk(startdir):
        for fname in fileshere:
            fpath = os.path.join(thisdir, fname)
            visitfile(fpath, searchkey)


def visitfile(fpath, searchkey):
    global fcount, vcount
    print(vcount+1, "=>", fpath)
    try:
        if not listonly:
            if os.path.splitext(fpath)[1] not in textexts:
                print('Skipping...', fpath)
            elif searchkey in open(fpath).read():
                input("{} has {}".format(fpath, searchkey))
                fcount += 1
    except Exception:
        print("Failed:", fpath, sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
    vcount += 1


if __name__ == '__main__':
    searcher(sys.argv[1], sys.argv[2])
    print("Found in {} files, visited {}".format(fcount, vcount))
