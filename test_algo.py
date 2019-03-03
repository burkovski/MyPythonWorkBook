import os
import random


class Arrive:
    def __init__(self):
            self.data = []

    def sort(self):
        if self.data:
            self.data.sort()

    def from_iter(self, any_iter):
        self.data = [int(x) for x in any_iter]

    def __str__(self):
        # self.sort()
        return "{}".format(self.data)


class Launcher:
    def __init__(self, arr_len, range_from, range_to, in_file, out_file, lines):
        self.arr_len = arr_len
        self.range_from = range_from
        self.range_to = range_to
        self.lines = lines
        self.in_file_path = in_file
        self.out_file_path = out_file

    def make_file(self):
        with open(self.in_file_path, 'w') as file:
            for line_num in range(self.lines):
                arr = [random.randint(self.range_from, self.range_to)
                       for _ in range(self.arr_len)]
                file.write(', '.join((str(x) if random.randint(0, 9) else 'SPAM' for x in arr)) + '\n')

    def test(self):
        with open(self.in_file_path) as in_file, open(self.out_file_path, 'w') as out_file:
            for line in in_file:
                my_arr = Arrive()
                try:
                    my_arr.from_iter(line.split(', '))
                    out_file.write("In data: {}\t".format(my_arr))
                    my_arr.sort()
                    out_file.write("Out data: {}\t".format(my_arr))
                    out_file.write("Status: OK!\n")
                except ValueError:
                    out_file.write("In data: INVALID!\t".format(my_arr))
                    out_file.write("Out data: NONE!\t")
                    out_file.write("Status: Invalid data!\n")


if __name__ == "__main__":
    launcher = Launcher(10, -20, 20, ".\\in_file.txt", ".\\out_file.txt", 5)
    launcher.make_file()
    launcher.test()
