import sys


def filter_files(name, func):
    with open(name) as in_file, open(name + '.out', 'w') as out_file:
        for line in in_file:
            out_file.write(func(line))


def filter_stream(func):
    for line in sys.stdin:
        print(func(line), end='')


if __name__ == '__main__':
    filter_stream(lambda line: line)