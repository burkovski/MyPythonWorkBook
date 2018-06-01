from math import factorial

sep_char = '-'

class Number:
    def __init__(self, value):
        self.value = value

    def fact(self, x=None):
        if x is None: x = self.value
        return factorial(x)

    def __str__(self):
        return ("\n+{0}+{1}+\n| Number     |{2:^30}|\n"
                "+{0}+{1}+\n| Factorial  |{3:^30}|\n"
                "+{0}+{1}+".format(
                 sep_char*12,
                 sep_char*30,
                 self.value,
                 self.fact(self.value)))

class Matrix(Number):
    def __init__(self, n):
        prompt = "\nEnter value for item:\n-> "
        matrix = [int(input(prompt)) for x in range(n)]
        super(Matrix, self).__init__(matrix)

    def fact(self, seq=None):
        if seq is None: seq = self.value
        return [Number.fact(self, x) for x in seq]

    def __str__(self):
        return ("\n+{0}+{1}+\n| Array      |{2:^30}|\n"
                "+{0}+{1}+\n| Factorials |{3:^30}|\n"
                "+{0}+{1}+\n".format(
                 sep_char*12,
                 sep_char*30,
                 ', '.join([str(x) for x in self.value]),
                 ', '.join([str(x) for x in self.fact(self.value)])))


if __name__ == "__main__":
    n = int(input("\nEnter the number:\n-> "))
    X = Number(n)
    Y = Matrix(n)
    print(X)
    print(Y)