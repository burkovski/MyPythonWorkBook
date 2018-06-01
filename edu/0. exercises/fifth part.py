def count_lines(file):
    count = 0
    file.seek(0)
    for line in file:
        count += 1
    return count

def count_chars(file):
    file.seek(0)
    count = 0
    for line in file:
        count += len(line)
    return count

def test(*, name="fifth part.py"):
    seplen = 13 + len(name)
    sepchar = '-'
    sepline = '+' + sepchar * seplen
    file = open(name)
    print(sepline)
    print("| In file: <{0}>\n| Lines: {1}\n| Characters: {2}".format(name, count_lines(file), count_chars(file)))
    print(sepline, end='\n\n')

if __name__ == "__main__":
    test()
    test(name='mytimer.py')