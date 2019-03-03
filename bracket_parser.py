import os
import sys

cmd_valid_args = {'-f': 'file_path'}


class BracketsParser:
    def __init__(self, file_path):
        self.path = file_path
        self.stack = []
        self.left_bracket = "{"
        self.right_bracket = "}"

    def parse_line(self, line, line_num):
        for chr in line:
            if chr == self.left_bracket:
                self.stack.append({"type": self.left_bracket,
                                   "line": line_num,
                                   "text": line})
            elif chr == self.right_bracket:
                if not self.stack or self.stack[-1]["type"] == self.right_bracket:
                    self.stack.append({"type": self.right_bracket,
                                       "line": line_num,
                                       "text": line})
                else:
                    self.stack.pop()

    def parse_file(self):
        with open(self.path, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                self.parse_line(line.rstrip(), line_num)

    def do_check(self):
        reply_path = os.path.abspath(self.path)
        try:
            self.parse_file()
        except FileNotFoundError:
            print("No such file or directory: '{}'.".format(reply_path))
        else:
            path, file = os.path.split(self.path)
            out_file = "result_{}.txt".format(file)
            if self.stack:
                template = "Error in file: '{path}';\n\t line: {line};\n\t text: '{text}'."
                for err_ln in self.stack:
                    reply = template.format(path=reply_path, **err_ln)
                    print(reply)
                    with open(out_file, 'w') as file: print(reply, file=file)
                if input("Do you want open file to edit? ") in {'y', 'Y'}:
                    os.system(self.path)
            else:
                reply = "File '{}' is correct.".format(reply_path)
                print(reply)
                with open(out_file, 'w') as file:
                    print(reply, file=file)


def launcher():
    if len(sys.argv) == 1:
        key, command = "-f", r"D:\Univ\ipz\hw\main.cpp"#sys.argv[1:]
        if key == '-f':
            BracketsParser(command).do_check()
            return
    print("Invalid command! Command should be: '{} -f <path to file>'".format(os.path.split(__file__)[1]))


if __name__ == "__main__":
    launcher()
