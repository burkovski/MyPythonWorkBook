"""
Отыскивает наибольший файл с исходным программным кодом на языке Python,
присутствующий в пути поиска модулей.
Пропускает каталоги, которые уже были просканированы; нормализует пути и регистр
символов, обеспечивая корректность сравнения; включает в выводимые результаты
счетчики строк. Здесь недостаточно использовать os.environ['PYTHONPATH']:
этот список является лишь подмножеством списка sys.path.
"""

import sys
import os
import pprint


trace = 0
visited = {}
all_sizes = []

for src_dir in sys.path:
    for (this_dir, subs_here, files_here) in os.walk(src_dir):
        if trace > 0: print(this_dir)
        this_dir = os.path.normpath(this_dir)
        fix_case = os.path.normcase(this_dir)
        if fix_case in visited:
            continue
        else:
            visited[fix_case] = True
        for file_name in files_here:
            if file_name.endswith('.py'):
                if trace > 1: print("...", file_name)
                pypath = os.path.join(this_dir, file_name)
                try:
                    pysize = os.path.getsize(pypath)
                except os.error:
                    print("skipping...", pypath, sys.exc_info()[0])
                else:
                    pylines = 0
                    for line in open(pypath, 'rb'): pylines += 1
                    all_sizes.append((pysize, pylines, pypath))

print("By size...")
all_sizes.sort()
pprint.pprint(all_sizes[:3])
pprint.pprint(all_sizes[-3:])

print("By lines...")
all_sizes.sort(key=lambda x: x[1])
pprint.pprint(all_sizes[:3])
pprint.pprint(all_sizes[-3:])
