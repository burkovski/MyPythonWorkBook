"""
Подсчитывает строки во всех файлах с исходными текстами программ в дереве
каталогов, указанном в командной строке, и выводит сводную информацию,
сгруппированную по типам файлов (по расширениям). Реализует простейший алгоритм
SLOC (source lines of code – строки исходного текста): если необходимо, добавьте
пропуск пустых строк и комментариев.
"""

import sys
import os
import pprint
from visitor import FileVisitor


class LineByType(FileVisitor):
    srcExts = []

    def __init__(self, trace=1):
        FileVisitor.__init__(self, trace=trace)
        self.srcLines = 0
        self.srcFiles = 0
        self.extSums = {ext: dict(files=0, lines=0) for ext in self.srcExts}

    def visit_source(self, fpath, ext):
        if self.trace:
            print(os.path.basename(fpath))
        lines = len([line for line in open(fpath, 'rb')])
        self.srcFiles += 1
        self.srcLines += lines
        self.extSums[ext]['files'] += 1
        self.extSums[ext]['lines'] += lines

    def visit_file(self, fpath):
        FileVisitor.visit_file(self, fpath)
        for ext in self.srcExts:
            if fpath.endswith(ext):
                self.visit_source(fpath, ext)
                break


class PyLines(LineByType):
    srcExts = ['.py', '.pyw']


class SourceLines(LineByType):
    srcExts = ['.py', '.pyw', '.cgi', '.html', '.c', '.cxx', '.h', '.i']


if __name__ == '__main__':
    walker = SourceLines()
    walker.run(sys.argv[1])
    print("Visited {} files and {} dirs".format(walker.fcount, walker.dcount))
    print("-" * 80)
    print("Source files=>{}, lines=>{}".format(walker.srcFiles, walker.srcLines))
    print("By Types:")
    pprint.pprint(walker.extSums)
    print("\nChecks sums:", end=' ')
    print(sum(x['lines'] for x in walker.extSums.values()), end=' ')
    print(sum(x['files'] for x in walker.extSums.values()))
    print("\nPython only walk:")
    walker = PyLines(trace=0)
    walker.run(sys.argv[1])
    pprint.pprint(walker.extSums)
