"""
Использование: 'python ...\Tools\visitor_cpall.py fromDir toDir trace?'
Действует подобно сценарию System\Filetools\cpall.py, но использует классы-
обходчики и функцию os.walk; заменяет строку fromDir на toDir перед всеми
именами, возвращаемыми обходчиком; предполагается, что изначально каталог toDir
не существует;
"""

import os
from visitor import FileVisitor
from cpall import copyfile


class CpallVisitor(FileVisitor):
    def __init__(self, from_dir, to_dir, trace=True):
        self.fromPath_len = len(from_dir) + 1
        self.to_dir = to_dir
        FileVisitor.__init__(self, trace=trace)

    def visit_dir(self, dpath):
        to_path = os.path.join(self.to_dir, dpath[self.fromPath_len:])
        if self.trace:
            print("d", dpath, "=>", to_path)
        os.mkdir(to_path)
        self.dcount += 1

    def visit_file(self, fpath):
        to_path = os.path.join(self.to_dir, fpath[self.fromPath_len:])
        if self.trace:
            print("f", fpath, '=>', to_path)
        copyfile(fpath, to_path)
        self.fcount += 1


if __name__ == '__main__':
    import sys
    import time

    from_dir, to_dir = sys.argv[1:3]
    trace = len(sys.argv) > 3
    print("Copying...")
    start = time.clock()
    walker = CpallVisitor(from_dir, to_dir, trace)
    walker.run(start_dir=from_dir)
    print("Copied", walker.fcount, 'files', walker.dcount, 'directories', end=' ')
    print('in', time.clock()-start, 'seconds')
