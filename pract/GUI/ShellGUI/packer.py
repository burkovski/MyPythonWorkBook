"""
упаковывает текстовые файлы в единый файл,
добавляя строки-разделители (простейшая архивация)
"""

import sys
import glob

marker = ':' * 20 + "textpak=>"         # надеемся, что это уникальная строка


def pack(ofile, ifiles):
    out_file = open(ofile, 'w')
    for file_name in ifiles:
        print("packing: {}".format(file_name))
        in_file = open(file_name, 'r').read()                   # открыть следующий входной файл
        if not in_file.endswith('\n'):                          # гарантировать наличие \n в конце
            in_file += '\n'
        out_file.write("{}{}\n".format(marker, file_name))      # записать строку-разделитель
        out_file.write(in_file)                                 # и содержимое входного файла


if __name__ == "__main__":
    in_files = []
    for pattern in sys.argv[2:]:
        in_files.extend(glob.glob(pattern))
    pack(sys.argv[1], in_files)                     # упаковать файлы, перечисленные в командной строке
