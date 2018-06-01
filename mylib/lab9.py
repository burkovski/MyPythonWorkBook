import sys


class Func:
    def __init__(self):
        self.coord = reader()
        self.x = [func_coord['x'] for func_coord in self.coord]
        self.y = [func_coord['y'] for func_coord in self.coord]
        self.z = [func_coord['z'] for func_coord in self.coord]

    def maxmin(self, test):
        tmp_x = test(self.x)
        tmp_y = test(self.y)
        tmp_z = test(self.z)
        return tmp_x, tmp_y, tmp_z

    def max_coord(self):
        return self.maxmin(max)

    def min_coord(self):
        return self.maxmin(min)


def reader(*, file_name="in_file.txt"):
    with open(file_name) as file:
        func_coord = []
        keys = ('x', 'y', 'z')
        for line in file:
            line = line.split()
            tmp_coord = {}
            for ix, key in enumerate(keys):
                tmp_coord.update({key: float(line[ix])})
            func_coord.append(tmp_coord)
        return func_coord


def writer(text, *, file_name="out_file.txt"):
    sys.stdout = open(file_name, 'w')
    line = lambda func_coord: "    ".join("{0:+010.3f}".format(func_coord[key]) for key in func_coord)
    res = "\n".join(line(func_coord) for func_coord in text)
    print(res)
    sys.stdout = sys.__stdout__
    # for line in text:
    #     for key in line:
    #         print("{0:+010.3f}".format(float(line[key])), end='    ')
    #     print()


func = Func()
writer(func.coord)
max_xval, max_yval, max_zval = func.max_coord()
max_xcoord = func.coord[func.x.index(max_xval)]
max_ycoord = func.coord[func.y.index(max_yval)]
max_zcoord = func.coord[func.z.index(max_zval)]
maximum = max_xcoord, max_ycoord, max_zcoord

min_xval, min_yval, min_zval = func.min_coord()
min_xcoord = func.coord[func.x.index(min_xval)]
min_ycoord = func.coord[func.y.index(min_yval)]
min_zcoord = func.coord[func.z.index(min_zval)]
minimum = min_xcoord, min_ycoord, min_zcoord