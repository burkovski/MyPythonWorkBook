import msvcrt
import os
import sys
import random

from mylib.stack import Stack


ENTER_CODE = 13
ESC_CODE = 27
ONE_CODE = 49
TWO_CODE = 50
THREE_CODE = 51
FOUR_CODE = 52


class Carriage:
    def __init__(self, carriage_type, number):
        self.carriage_type = carriage_type
        self.__number = number

    def get(self):
        return self.carriage_type, self.__number

    def __set(self, carriage_type, number):
        self.carriage_type = carriage_type
        self.__number = number


def key_code():  # Возвращает код нажатой клавиши
    while not msvcrt.kbhit(): pass
    return ord(msvcrt.getch())


def clear_shell():  # Очистка консоли
    os.system("cls") if sys.platform == "win32" else os.system("clear")


def menu_display():
    msg = ("<1> Create train"
           "\n<2> Sort train"
           "\n<3> Display train"
           "\n<4> Length of trains")
    sepline('-', 20)
    print(msg)
    sepline('-', 20)


def sepline(sepchar, seplen):   # Отображение линии-разделителя
    print(sepchar * seplen)


def create_seq():   # Выбор режима создания состава - вручную или автоматически(рандом)
    clear_shell()
    sepline('-', 41)
    print("Press <1> for created train automatically"
          "\nPress <2> for created train by yourself")
    sepline('-', 41)
    choice = key_code()
    if choice == ONE_CODE:
        create_auto()
    elif choice == TWO_CODE:
        create()


def create_auto():  # Автоматическое создание состава
    clear_shell()
    while True:
        length = input("Enter length of train(not too large):\n-> ")
        if check_input(length):
            length = int(length)
            clear_shell()
            break

    for i in range(length):
        instance = Carriage(random.randint(1, 2), random.randint(1000, 9999))
        train.push(instance)


def create():   # Создание вручную
    while True:
        carriage_type = input("\nEnter carriage type(1 or 2):\n-> ")
        if not check_input(carriage_type, start=1, stop=2):
            continue
        number = input("Enter carriage number(1000 -> 9999):\n-> ")
        if not check_input(number, start=1000, stop=9999):
            continue

        instance = Carriage(carriage_type, number)
        train.push(instance)

        print("\nPress <ESC> for exit from creating train...")
        if key_code() == ESC_CODE: break
        clear_shell()


def check_input(integer, *, start=None, stop=None):   # Проверка ввода: является ли числом, наличие выхода за границы
    if integer.isdigit():
        if start and stop:
            if start <= int(integer) <= stop:
                return True
            else:
                print("<ValueError: Out of range!>\n")
                return False
        else:
            return True
    else:
        print("<ValueError: You did not enter a number!>\n")
        return False


def choice_stack():     # Выбор состава, для отображения
    while True:
        clear_shell()
        sepline('-', 53)
        print("Press <1> for choice unsorted train"
              "\nPress <2> for choice train with first-type carriages"
              "\nPress <3> for choice train with second-type carriages")
        sepline('-', 53)

        choice = key_code()
        if choice == ONE_CODE:
            display(train)
        elif choice == TWO_CODE:
            display(first_train)
        elif choice == THREE_CODE:
            display(second_train)

        print("Press <ESC> for exit from creating train...")
        if key_code() == ESC_CODE: break


def display(trn):   # Непосредственно, само отображение
    if trn.is_empty():
        print("<Stack is empty!>")
        return

    sepline('-', 24)
    for carriage in reversed(trn.stack):
        print("Type: {0} <=> Number: {1}".format(*carriage.get()))
    sepline('-', 24)


def sort_train():   # Создание двух составов(сортировка по типу)
    for carriage in reversed(train.stack):
        if carriage.carriage_type == 1:
            first_train.push(carriage)
        else:
            second_train.push(carriage)
        train.pop()


def len_train():    # Отобразит длину каждого состава в данный момент
    clear_shell()
    sepline('-', 35)
    print("Unsorted train length = {0}\n"
          "First-type carriages train len = {1}\n"
          "Second-type carriages train len = {2}".format(train.len_stack(),
                                                         first_train.len_stack(),
                                                         second_train.len_stack()))
    sepline('-', 35)


def menu():         # Меню программы: выбор функций, выход
    while True:
        clear_shell()
        menu_display()
        choice = key_code()
        if choice == ONE_CODE:
            create_seq()
        elif choice == TWO_CODE:
            sort_train()
        elif choice == THREE_CODE:
            clear_shell()
            choice_stack()
        elif choice == FOUR_CODE:
            len_train()
        else:
            print("\nNo function for your choice!")

        print("\nPress <ESC> for exit from program...")
        if key_code() == ESC_CODE: break



if __name__ == "__main__":
    train = Stack()
    first_train = Stack()
    second_train = Stack()
    menu()