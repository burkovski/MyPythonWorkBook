"""
##############################################################################
Порядок использования: “python diffall.py dir1 dir2”.
Выполняет рекурсивное сравнение каталогов: сообщает об уникальных файлах,
существующих только в одном из двух каталогов, dir1 или dir2; сообщает о файлах
с одинаковыми именами и с разным содержимым, присутствующих в каталогах dir1
и dir2; сообщает об разнотипных элементах с одинаковыми именами, присутствующих
в каталогах dir1 и dir2; то же самое выполняется для всех подкаталогов
с одинаковыми именами, находящихся внутри деревьев каталогов dir1
и dir2. Сводная информация об обнаруженных отличиях помещается в конец вывода,
однако в процессе поиска в вывод добавляется дополнительная информация об
отличающихся и уникальных файлах с метками “DIFF” и “unique”. Новое: (в 3
издании) для больших файлов введено ограничение на размер читаемых блоков в 1
Мбайт, (3 издание) обнаруживаются одинаковые имена файлов/каталогов, (4 издание)
исключены лишние вызовы os.listdir() в dirdiff.comparedirs() за счет передачи
результатов.
##############################################################################
"""

import os
import dirdiff

blocksize = 1024 * 1024


def intersect(seq1, seq2):
    """
    Возвращает все элементы, присутствующие одновременно в seq1 и seq2;
    выражение set(seq1) & set(seq2) возвращает тот же результат, но множества
    являются неупорядоченными коллекциями, поэтому при их использовании может
    быть утерян порядок следования элементов, если он имеет значение для
    некоторых платформ
    """
    return [item for item in seq1 if item in seq2]


def comparetrees(dir1, dir2, diffs, verbose=False):
    """
    Сравнивает все подкаталоги и файлы в двух деревьях каталогов;
    для предотвращения кодирования/декодирования содержимого и преобразования
    символов конца строки использует двоичный режим доступа к файлам,
    так как деревья могут содержать произвольные двоичные и текстовые файлы;
    функции listdir может потребоваться передавать аргумент типа bytes, если
    могут встречаться имена файлов, недекодируемые на других платформах
    """
    # сравнить списки с именами файлов
    print("-" * 20)
    names1 = os.listdir(dir1)
    names2 = os.listdir(dir2)
    if not dirdiff.comparedirs(dir1, dir2, names1, names2):
        diffs.append("unique files at {} - {}".format(dir1, dir2))

    print("Comparing contents")
    common = intersect(names1, names2)
    missed = common.copy()

    # сравнить содержимое файлов с одинаковыми именами
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            missed.remove(name)
            file1 = open(path1, 'rb')
            file2 = open(path2, 'rb')
            while True:
                bytes1 = file1.read(blocksize)
                bytes2 = file2.read(blocksize)
                if not bytes1 and not bytes2:
                    if verbose: print(name, "matches")
                    break
                if bytes1 != bytes2:
                    diffs.append("files differ at {} - {}".format(path1, path2))
                    print(name, "DIFFERS")
                    break

    # рекурсивно сравнить каталоги с одинаковыми именами
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparetrees(path1, path2, diffs, verbose)

    # одинаковые имена, но оба не являются одновременно файлами или каталогами?
    for name in missed:
        diffs.append("files missed at {} - {}: {}".format(dir1, dir2, name))
        print(name, "DIFFERS")


if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    diffs = []
    comparetrees(dir1, dir2, diffs, True)
    print("=" * 40)
    if not diffs:
        print("No diffs found")
    else:
        print("Diffs found:", len(diffs))
        for diff in diffs:
            print("\t-", diff)
