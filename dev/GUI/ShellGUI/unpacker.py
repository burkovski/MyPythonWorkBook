"""
распаковывает архивы, созданные сценарием
packer.py (простейшие архивы текстовых файлов)
"""

import sys
from packer import marker       # использовать общую строку-разделитель

mlen = len(marker)              # имена файлов следуют за строкой-разделителем


def unpack(ifile, prefix="new_"):
    for line in open(ifile):                            # по всем строкам входного файла
        if line[:mlen] == marker:                       # строка-разделитель?
            file_name = prefix + line[mlen:-1]          # создать новый выходной файл
            print("creating: {}".format(file_name))
            output = open(file_name, 'w')
        else:
            output.write(line)                          # действительные строки записать


if __name__ == "__main__":
    unpack(sys.argv[1])
