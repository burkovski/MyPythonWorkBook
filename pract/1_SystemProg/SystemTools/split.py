"""
##############################################################################
разрезает файл на несколько частей; сценарий join.py объединяет эти части в один
файл; данный сценарий является настраиваемой версией стандартной команды split
в Unix; поскольку сценарий написан на языке Python, он с тем же успехом может
использоваться в Windows и легко может быть модифицирован; благодаря тому, что
он экспортирует функцию, его логику можно импортировать и повторно использовать
в других приложениях;
##############################################################################
"""

import sys
import os


kilobytes = 1024
megabytes = kilobytes * 1000
chunk_size = int(1.4 * megabytes)


def split(fromfile, todir, chunk_size = chunk_size):
    if not os.path.exists(todir):
        os.mkdir(todir)             # создать каталог для фрагментов
    else:
        for fname in os.listdir(todir):     # удалить все существующие файлы
            os.remove(fname)

    partnum = 0
    infile = open(fromfile, 'rb')

    while True:
        chunk = infile.read(chunk_size)
        if not chunk: break
        partnum += 1
        filename = os.path.join(todir, "part{0:04}".format(partnum))
        with open(filename, 'wb') as fileobj:
            fileobj.write(chunk)
    infile.close()
    assert partnum <= 9999
    return partnum


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "-help":
        print("Use: split.py [file-to-split target-dir [chunksize]]")
    else:
        if len(sys.argv) < 3:
            interactive = True
            fromfile = input("File to be split?\n-> ")    # ввод данных, если запущен щелчком мыши
            todir = input("Directory to store part files?\n-> ")
        else:
            interactive = False
            fromfile, todir = sys.argv[1:3]
            if len(sys.argv) == 4: chunk_size = int(sys.argv[3])
        absform, absto = map(os.path.abspath, [fromfile, todir])
        print("Splitting", absform, "to", absto, "by", chunk_size)

        try:
            parts = split(fromfile, todir, chunk_size)
        except Exception:
            print("Error during split:")
            print(sys.exc_info()[0], sys.exc_info()[1])
        else:
            print("Split finished:", parts, "parts are in", absto)
        if interactive: input("Press <Enter> to exit!")