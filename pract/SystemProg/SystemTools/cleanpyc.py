"""
удаляет все файлы .pyc с байт-кодом в дереве каталогов: аргумент командной
строки, если он указан, интерпретируется как корневой каталог, в противном
случае корневым считается текущий рабочий каталог
"""

import os
import sys

findonly = False
rootdir = os.getcwd() if len(sys.argv) == 1 else sys.argv[1]
found = removed = 0


for (this_dir, dirs_here, files_here) in os.walk(rootdir):
    for fname in files_here:
        if fname.endswith(".pyc"):
            fullname = os.path.join(this_dir, fname)
            print('=>', fullname)
            if not findonly:
                try:
                    os.remove(fullname)
                    removed += 1
                except Exception:
                    type_, inst = sys.exc_info()[:2]
                    print('*' * 4, "Failed:", fname, type_, inst)
            found += 1


if __name__ == '__main__':
    print("Found:", found, "files, removed:", removed)