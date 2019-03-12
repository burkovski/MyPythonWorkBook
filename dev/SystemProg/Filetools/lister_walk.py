import os
import sys


def lister(root):   # Для корневого каталога
    for (dirname, subshere, fileshere) in os.walk(root):    # Перечисляет
        print('[' + dirname + ']')                          # Каталоги в дереве
        for fname in fileshere:                         # Вывод файлов в каталоге
            path = os.path.join(dirname, fname)         # Добавить имя каталога
            print(path)


if __name__ == '__main__':
    lister(sys.argv[1])             # Получить имя каталога из командной строки
