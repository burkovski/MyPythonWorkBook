"""
Отыскивает наибольший файл заданного типа в произвольном дереве каталогов.
Пропускает каталоги, которые уже были просканированы; перехватывает ошибки;
добавляет возможность вывода трассировки поиска и подсчета строк.
Кроме того, использует множества, итераторы файлов и генераторы, чтобы избежать
загрузки содержимого файлов целиком, и пытается обойти проблемы, возникающие при
выводе недекодируемых имен файлов/каталогов.
"""

import os
import pprint
from sys import argv, exc_info


trace = 1                                   # 0=выкл., 1=каталоги, 2=+файлы
dir_name, ext_name = os.curdir, '.py'       # по умолчанию файлы .py в cwd
if len(argv) > 1: dir_name = argv[1]        # например: C:\, C:\Python31\Lib
if len(argv) > 2: ext_name = argv[2]        # например: .pyw, .txt
if len(argv) > 3: trace    = int(argv[3])   # например: “. .py 2”


def try_print(arg):
    try:
        print(arg)
    except UnicodeEncodeError:
        print(arg.encode())


visited   = set()
all_sizes = []

for (this_dir, subs_here, files_here) in os.walk(dir_name):
    if trace: try_print(this_dir)
    this_dir = os.path.normpath(this_dir)
    fix_name = os.path.normcase(this_dir)
    if fix_name in visited:
        if trace: try_print("skipping..." + this_dir)
    else:
        visited.add(fix_name)
        for file_name in files_here:
            if file_name.endswith(ext_name):
                if trace > 1: try_print("+++" + file_name)
                full_name = os.path.join(this_dir, file_name)
                try:
                    byte_size = os.path.getsize(full_name)
                    line_size = sum(+1 for line in open(full_name, 'rb'))
                except Exception:
                    print("Error...", exc_info()[0])
                else:
                    all_sizes.append((byte_size, line_size, full_name))

for (title, key) in [('bytes', 0), ('lines', 1)]:
    print("\nBy {}...".format(title))
    all_sizes.sort(key=lambda x: x[key])
    print("\tThe smallest:", *all_sizes[:3], sep='\n\t\t')
    print("\tThe biggest:", *all_sizes[-3:], sep='\n\t\t')


print("\nFiles have been viewed:", len(all_sizes))
res = 0
for file in all_sizes: res += file[0]
print("Total files size {} bytes".format(res))
print("Weight of all_sizes {} bytes".format(all_sizes.__sizeof__()))
