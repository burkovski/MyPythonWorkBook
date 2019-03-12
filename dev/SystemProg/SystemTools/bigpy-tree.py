"""
Отыскивает наибольший файл с исходным программным кодом на языке Python в дереве
каталогов.
Поиск выполняется в каталоге стандартной библиотеки,
отображение результатов
выполняется с помощью модуля pprint.
"""

import os
import sys
import pprint


trace = False
if sys.platform.startswith("win"):
    dir_name = r"C:\Python\Lib"
else:
    dir_name = "usr/lib/python"


all_sizes = []
for (this_dir, subs_here, files_here) in os.walk(dir_name):
    if trace:
        print(this_dir)
    for file_name in files_here:
        if file_name.endswith(".py"):
            if trace: print("...", file_name)
            full_name = os.path.join(this_dir, file_name)
            full_size = os.path.getsize(full_name)
            all_sizes.append((full_size, full_name))

all_sizes.sort()
pprint.pprint(all_sizes[:2])
pprint.pprint(all_sizes[-2:])
