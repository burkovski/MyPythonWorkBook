class Complex:
    def __init__(self, real, imag):
        self.real = real            # Действительная часть
        self.imag = imag            # Мнимая

    def __str__(self):              # Перегрузим для удобочитаемого вывода атрибутов
        if self.real == 0:          # Если мнимая часть равна 0:
            res = "{0}j".format(self.imag)    # Вывод в виде (Bj)
        else:                       # Иначе => (A+/-Bj)
            res = "({0}{1:+}j)".format(self.real, self.imag)
        return res                  # Вернуть строку вызывающей функии/методу

    @staticmethod
    def __op_checker(other, op_chr):    # Проверка типов операндов
        op_allowed = tuple('*')         # Разрешим умножать на int
        if isinstance(other, Complex):  # Complex?
            return True                 # OK!
        elif isinstance(other, int):    # int?
            if op_chr in op_allowed:    # Рахрешенная операция?
                return True             # OK!
        # Выхода не произошло => ошибка
        Complex.__error_msg(other, op_chr)  # Бросить исключение

    @staticmethod
    def __error_msg(other, op_chr):     # Возбудить исключение
        # В конструктор класса исключения отправим информацию об ошибке
        raise TypeError("<unsupported operand type(s) for {0}: "
                        "'Complex' and '{1}'>".format(op_chr, other.__class__.__name__))

    def __add__(self, other):       # Complex + other
        if Complex.__op_checker(other, '+'):        # other is Complex?
            return Complex(self.real + other.real,  # OK!
                           self.imag + other.imag)

    def __sub__(self, other):       # Complex - other
        if Complex.__op_checker(other, '-'):
            return Complex(self.real - other.real,
                           self.imag - other.imag)

    def __mul__(self, other):       # Complex * other
        if Complex.__op_checker(other, '*'):        # Complex - Complex или int
            if isinstance(other, Complex):          # other is Complex?
                # => return Complex * Complex
                return Complex(self.real * other.real - self.imag * other.imag,
                               self.real * other.imag + self.imag * other.real)
            else:                   # other is int.
                return self.__mul_int(other)        # Complex * int

    def __mul_int(self, other):     # Умножит комплексное и целое
        return Complex(self.real * other, self.imag * other)

    def __eq__(self, other):        # Равенство
        if Complex.__op_checker(other, '=='):
            return self.real == other.real and self.imag == other.imag

    def __ne__(self, other):        # НЕравенство
        if Complex.__op_checker(other, '!='):
            return self.real != other.real and self.imag != other.imag

    def __neg__(self):              # Унарный минус
        return Complex(self.real, -self.imag)


if __name__ == '__main__':  # Код самопроверки
    x = Complex(1, 2)
    y = Complex(2, 4)
    print(x + y)
    # print(x + 99)       # Ошибка!
    print(x * y)
    print(x * 2)          # OK!
    # print(x * 3.1415)   # Ошибка!
    print(x - y)
    # print(x - 88)       # Ошибка!
    print(-x)
    # print(+x)           # Ошибка!