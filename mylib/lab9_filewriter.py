import math
NUM = 10

with open("in_file.txt", 'w') as file:
    for x in range(1, NUM):
        line = "{0} {1:10.3f} {2:10.3f}\n".format(x, math.pow(x, 2), math.sqrt(x)/x)
        file.write(line)