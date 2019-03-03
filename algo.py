import os
import sys
import random


class MinMaxArrive:
    def __init__(self, file_path=None):
        self.arrive = None
        self.path = file_path

    def open_file(self):
        try:
            with open(self.path, 'r') as file:
                line = file.readline().rstrip()
                self.arrive = [int(x) for x in line.split()]
        except FileNotFoundError:
            return "No such file or directory! {}".format(self.path)
        except ValueError:
            return "Invalid data in file: {}".format(os.path.abspath(self.path))

    def __str__(self):
        return self.get_arrive(sort=True)

    def get_arrive(self, *, sort=False):
        if self.arrive:
            reply = "{}".format(sorted(self.arrive) if sort else self.arrive)
        else:
            reply = "No data for display!"
        return reply


if __name__ == "__main__":
    arr = MinMaxArrive(sys.argv[1])
    print(arr)
    # with open("in_file.txt", 'w') as file:
    #     file.write(' '.join(str(random.randint(-99, 99)) for _ in range(50)) + '\n')
