"""
Отыскивает наибольший файл с исходным программным кодом на языке Python
в единственном каталоге.
Поиск выполняется в каталоге стандартной библиотеки
Python для Windows, если
в аргументе командной строки не был указан какой-то другой каталог.
"""

import os
import sys
import glob

dir_name = r"C:\Python\Lib" if len(sys.argv) == 1 else sys.argv[1]

all_sizes = []
for file_name in glob.iglob(dir_name + os.sep + '*.py'):
    file_size = os.path.getsize(file_name)
    all_sizes.append((file_size, file_name))

all_sizes.sort()
print("Smaller:\n\t", all_sizes[:2])
print("Bigger:\n\t", all_sizes[-2:])

