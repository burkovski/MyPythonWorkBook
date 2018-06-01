print("str uniq methods: {}".format(set(dir("abc")) - set(dir(b"abc"))))   # Методы, уникальные для str
print("bytes uniq methods: {}\n".format(set(dir(b"abc")) - set(dir("abc"))))   # Методы, уникальные для bytes

B = b"spam"     # Посдеовательность целых коротких чисел
print("B = {}".format(B))   # Выводится как послдеовательность ASCII
print("B[0]: {}".format(B[0]))    # Операция индексирования вернет целое число
print("chr(B[0]): {}".format(chr(B[0])))    # Выведет символ, соотвествующий целому числу
print("list(B): {}\n".format(list(B)))    # Выведет целочисленные значения всех байтов

B = b"abc"      # Литеральное выражение
print("B = {}".format(B))
B = bytes("abc", "ascii")   # Вызов конструктора bytes, с указанием кодировки
print("B = {}".format(B))
B = bytes([97, 98, 99])     # Превратить последовательность целых чисел в строку байтов
print("B = {}".format(B))
B = "abc".encode()          # Метод кодровки str в bytes
print("B = {}\n".format(B))

print("B.replace(b'bc', b'XY'): {}".format(B.replace(b"bc", b"XY")))    # Должны передаваться объекты допустимых типов
print("b'ab'.decode() + 'cd': {}".format(b'ab'.decode() + 'cd'))    # bytes в str для конкатенации
print("b'ab' + 'cd'.encode(): {}".format(b'ab' + 'cd'.encode()))    # str в bytes для конкатенации
print("b'ab' + bytes('cd', 'ascii'): {}\n".format(b'ab' + bytes('cd', 'ascii')))  # str в bytes



S = "spam"
print("S = {}".format(S))
C = bytearray(S, 'ascii')   # Для преобразрвания str в bytearray необходимо указать кодировку
print("bytearray(S, 'ascii'): {}".format(C))
print("bytearray(C): {}".format(C))
print("C = {}".format(C))
print("C[0]: {}".format(C[0]))
C[1] = ord('c')
print("C[0] = ord('c'): {}".format(C))
C[-1] = b'n'[0]
print("C[-1] = b'n'[0]: {}".format(C))
C.append(ord('i'))
print("C.append(ord('i')): {}".format(C))
C.extend(b"ng")
print("C.extend(b'ng'): {}\n".format(C))



file = open('temp', 'w')
size = file.write('abc\n')
file.close()
file = open("temp")
text = file.read()
print("in <temp> file: {}size: '{}' bytes\n".format(text, size))

open('temp', 'w').write('abd\n')    # Запись в текстовом режиме: передается объект str
print(open('temp', 'r').read(), end='')     # Чтение в текстовом режиме: возвращает объект str
print(open('temp', 'rb').read())    # Чтение в двоичном режиме: возвращает объект bytes
open('temp', 'wb').write(b'abc\n')      # Запись в двоичном режиме: передается объект bytes
print(open('temp', 'r').read(), end='')     # Текстовый режимчтения, возвращается объект str
print(open('temp', 'rb').read())        # Двоичный режим чтения, возвращается объект bytes



S = "A\xc4B\xe8C"   # Строка из 5 байт, включает не ASCII символы
print("\nS = {}".format(S))
L = S.encode('latin-1')     # 5 байт
print("L = {}; len(L): {}".format(L, len(L)))
U = S.encode('utf-8')       # 7 байт
print("U = {}; len(U): {}".format(U, len(U)))
open('latindata', 'w', encoding='latin-1').write(S)
open('utf8data', 'w', encoding='utf-8').write(S)
print(open('latindata', 'rb').read())   # Прочитать двоичные данные
print(open('utf8data', 'rb').read())    # Содержимое файлов отличается
print(open('latindata', 'r', encoding='latin-1').read())    # Декодировние при чтении
print(open('utf8data', 'r', encoding='utf-8').read())