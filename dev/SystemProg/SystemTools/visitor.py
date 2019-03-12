"""
##############################################################################
Тест: 'python ...\Tools\visitor.py dir testmask [строка]'. Использует
классы и подклассы для сокрытия деталей использования функции os.walk при
обходе и поиске; testmask – битовая маска, каждый бит в которой определяет
тип самопроверки; смотрите также: подклассы visitor_*/.py; вообще подобные
фреймворки должны использовать псевдочастные имена вида __X, однако в данной
реализации все имена экспортируются для использования в подклассах и клиентами;
переопределите метод reset для поддержки множественных, независимых объектов-
обходчиков, требующих обновлений в подклассах;
##############################################################################
"""

import os
import sys


class FileVisitor:
    """
    Выполняет обход всех файлов, не являющихся каталогами, ниже startDir
    (по умолчанию '.'); при создании собственных обработчиков
    файлов/каталогов переопределяйте методы visit*; аргумент/атрибут context
    является необязательным и предназначен для хранения информации,
    специфической для подкласса; переключатель режима трассировки trace: 0 -
    нет трассировки, 1 - подкаталоги, 2 – добавляются файлы
    """
    def __init__(self, context=None, trace=2):
        self.fcount  = 0
        self.dcount  = 0
        self.context = context
        self.trace   = trace

    def run(self, start_dir=os.curdir, reset=True):
        if reset:
            self.reset()
        for (this_dir, dirs_here, files_here) in os.walk(start_dir):
            self.visit_dir(this_dir)
            for fname in files_here:                        # для некаталогов
                fpath = os.path.join(this_dir, fname)       # fname не содержит пути
                self.visit_file(fpath)

    def reset(self):            # используется обходчиками,
        self.fcount = 0         # выполняющими обход независимо
        self.dcount = 0

    def visit_dir(self, dir_path):      # вызывается для каждого каталога
        self.dcount += 1                # переопределить или расширить
        if self.trace:
            print(dir_path, "...")

    def visit_file(self, file_path):    # вызывается для каждого файла
        self.fcount += 1                # переопределить или расширить
        if self.trace > 1:
            print(self.fcount, "=>", file_path)


class SearchVisitor(FileVisitor):
    """
    Выполняет поиск строки в файлах, находящихся в каталоге startDir и ниже;
    в подклассах: переопределите метод visit_match, списки расширений, метод
    candidate, если необходимо; подклассы могут использовать testexts, чтобы
    определить типы файлов, в которых может выполняться поиск (но могут также
    переопределить метод candidate, чтобы использовать модуль mimetypes для
    определения файлов с текстовым содержимым: смотрите далее)
    """
    textexts = ['.txt', '.py', '.pyw', '.html', '.c', '.h']     # допустимые расш.
    skipexts = []                                               # или недопустимые

    def __init__(self, search_key, trace=2):
        FileVisitor.__init__(self, search_key, trace)
        self.scount = 0

    def reset(self):            # в независимых обходчиках
        self.scount = 0

    def candidate(self, fname):
        ext = os.path.splitext(fname)[1]
        if self.textexts:                   # если допустимое расширение
            return ext in self.textexts
        else:                               # или, если недопустимое
            return ext not in self.skipexts

    def visit_file(self, fname):                # поиск строки
        FileVisitor.visit_file(self, fname)
        if not self.candidate(fname):
            if self.trace:
                print("Skipping", fname)
        else:
            text = open(fname, 'rb').read()
            if self.context.encode() in text:
                self.visit_match(fname, text)
                self.scount += 1

    def visit_match(self, fname, text):           # обработка совпадения
        print("{} has {}".format(fname, self.context))


if __name__ == '__main__':
    dolist   = 1
    dosearch = 2
    donext   = 4

    def self_test(test_mask):
        if test_mask & dolist:
            visitor = FileVisitor(trace=2)
            visitor.run(sys.argv[2])
            print("Visited {} files and {} dirs".format(
                visitor.fcount,
                visitor.dcount
            ))

        if test_mask & dosearch:
            visitor = SearchVisitor(sys.argv[3], trace=0)
            visitor.run(sys.argv[2])
            print("Found in {} files, visited {}".format(
                visitor.scount,
                visitor.fcount
            ))

    self_test(int(sys.argv[1]))
