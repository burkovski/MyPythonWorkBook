import unittest
import algo


file_path = r"D:\Projects\Python\in_file.txt"
invalid_file_path = r"D:\Projects\Python\no_file.txt"
empty_file_path = r"D:\Projects\Python\empty_file.txt"
invalid_data_file_path = r"D:\Projects\Python\invalid_file.txt"


def arr_from_file(path):
    with open(path, 'r') as file:
        arr = file.readline().split()
        return sorted((int(item) for item in arr))


arr = arr_from_file(file_path)


class AlgoUnittest(unittest.TestCase):
    def test_openfile(self):
        self.assertEqual(algo.MinMaxArrive(invalid_file_path).open_file(),
                         "No such file or directory! {}".format(invalid_file_path))

    def test_invalid_data(self):
        self.assertEqual(algo.MinMaxArrive(invalid_data_file_path).open_file(),
                         "Invalid data in file: {}".format(invalid_data_file_path))

    def test_empty_file(self):
        minmax_arr = algo.MinMaxArrive(empty_file_path)
        minmax_arr.open_file()
        self.assertEqual(minmax_arr.__str__(),
                         "No data for display!")

    def test_show(self):
        minmax_arr = algo.MinMaxArrive(file_path)
        minmax_arr.open_file()
        self.assertEqual(minmax_arr.__str__(),
                         str(arr))


AlgoUnittest().test_empty_file()