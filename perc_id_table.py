import re
import os
import sys


class FakeTokenException(BaseException):
    pass


class IdentifierTable:
    def __init__(self, f_path, tm_str, gr_names):
        self.table = {}
        self.path = f_path
        self.pattern = re.compile(tm_str)
        self.group_names = tuple(name for name in gr_names)

    def parse_file(self, *, share_exception=False):
        with open(self.path) as file:
            for ix, line in enumerate(file, start=1):
                try:
                    yield self.parse_str(line, ix)
                except FakeTokenException as exc:
                    if share_exception: raise
                    print(exc)
                    return

    def parse_str(self, any_str, line_num):
        match = self.pattern.match(any_str)
        if match:
            return {k: match.group(k) for k in self.group_names}
        else:
            exc_str = "FakeTokenException:\n\tfile {};\n\tline {}: {};"
            raise FakeTokenException(exc_str.format(self.path, line_num, any_str.rstrip()))

    def make_table(self, *, share_exception=False):
        self.table = {line[self.group_names[0]]: (line[self.group_names[1]])
                      for line in self.parse_file(share_exception=share_exception)}

    def write_table(self, path=None):
        if not self.table:
            try:
                self.make_table(share_exception=True)
            except FakeTokenException as exc:
                print(exc)
                return
        if not path:
            dir_name, file_name = os.path.split(self.path)
            path = os.path.join(dir_name, "table_"+file_name)
        template = "| {0:<15}| {1:<10}| {2:<10}|"
        sep_chr = '-'
        sep_str = "+{}+{}+{}+".format(sep_chr*16, sep_chr*11, sep_chr*11)
        hdr = template.format("KEY", "NAME", "VALUE")
        with open(path, 'w') as file:
            sys.stdout = file
            print(sep_str)
            print(hdr)
            print(sep_str)
            for id_name in self.table:
                id_val = self.table[id_name]
                print(template.format(hash(id_name), id_name, id_val))
                print(sep_str)
            sys.stdout = sys.__stdout__


if __name__ == "__main__":
    group_names = ("var_id", "var_val")
    raw_str = r"^(?P<{0}>\w+)\s*=\s*(?P<{1}>\d+.?\d+%)\s*$"
    template_str = raw_str.format(*group_names)
    id_table = IdentifierTable(r"C:\Users\HP\Documents\ids_perc.txt", template_str, group_names)
    id_table.write_table()
