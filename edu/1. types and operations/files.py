import pickle
import struct

myfile = open("myfile.txt", 'w')        # Открывает файл (создает/очищает)
myfile.write("hello file file\n")       # Записывает строку текста
myfile.write("goodbye file file\n")
myfile.close()                          # Выталкивает выходные буферы на диск


myfile = open("myfile.txt")             # Открывает файл: 'r' - по умолчанию
string = myfile.readline()              # Читает строку
print(string, end='')
string = myfile.readline()              # Продолжает чтение со следующей строки
print(string, end='')
string = myfile.readline()
print('/' + string + '/', end='\n\n')   # Пустая строка - конец фала
myfile.close()

myfile = open("myfile.txt")
print(myfile.read())                    # Чтение файла целиком
myfile.close()

for line in open("myfile.txt"):         # Итератор файла
    print(line, end='')
print('')


data = open("data.bin", 'wb')                   # Открыть двоичный файл для записи
data.write(b"\x00\x00\x00\x07spam\x00\x08")     # Запись в файл
data = open("data.bin", 'rb')                   # Открыть двоичный файл для чтения
print(data.read())


X, Y, Z = 43, 44, 45            # Объекты языка Python должны записыаться в файл только в виде строк
S = 'Spam'
D = {'a': 1, 'b': 2}
L = [1, 2, 3]
F = open("datafile.txt", 'w')                  # Создает файл для записи
F.write(S + '\n')                              # Строки в фале должны завершаться симолом '\n'
F.write("{0}, {1}, {2}\n".format(X, Y, Z))     # Преобразует числа в строки
F.write(str(D) + '\n')                         # Преобразует словарь и список в строку для записи в файл
F.write(str(L) + '\n')
F.close()

chars = open("datafile.txt").read()     # Отображение строки в неформатированом виде
print('\n' + chars)                     # Удобочитаемое представление

F = open("datafile.txt")                # Обратное преобразование
line = F.readline()                     # Прочитать одну строку
S = line.rstrip()                       # Удалить завершающуий символ '\n'
print(S)
tmp = [int(val) for val in F.readline().split(', ')]       # Обратное преобразование в список
X = tmp[0]
Y = tmp[1]
Z = tmp[2]
del tmp
print(X, Y, Z)
D = eval(F.readline())      # Преобразовать строку в объект словаря
print(D)
L = eval(F.readline())      # Преобразовать строку в объект списка
print(L)
F.close()


D = {'a': 1, 'b': 2}
F = open("datafile.pkl", 'wb')
pickle.dump(D, F)                           # Модуль pickle запишет в файл любой объект
F.close()
F = open("datafile.pkl", 'rb')
print("\ndatafile.pkl:", pickle.load(F), '\n')    # Загружает любой объект из файла


F = open("data.bin", 'wb')                    # Открыть файл для записи в двоичном режиме
data = struct.pack(">i4sh", 7, b"spam", 8)    # Создаст пакет двоичных даных
print("Packed data:", data)
F.write(data)                                 # Записать строку байтов
F.close()

F = open("data.bin", 'rb')
data = F.read()                          # Получить упакованые двоичные даные
print("Unpacked data:", data)
values = struct.unpack(">i4sh", data)    # Преобразовать двоичные даные в объекты
print("Reformat data:", values, '\n')


with open("datafile.txt") as myfile:    # Менеждер контекста with...as позволяет не использовать метод close()
    for line in myfile:
        print(line, end='')
