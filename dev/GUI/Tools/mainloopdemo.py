"""
демонстрирует запуск двух отдельных циклов mainloop; каждый из них возвращает
управление после того как главное окно будет закрыто; ввод пользователя
сохраняется в объекте Python перед тем, как графический интерфейс будет
закрыт; обычно в программах с графическим интерфейсом настройка виджетов
и вызов mainloop выполняется всего один раз, а вся их логика распределена
по обработчикам событий; в этом демонстрационном примере вызовы функции
mainloop производятся для обеспечения модальных взаимодействий с пользователем
из программы командной строки; демонстрирует один из способов добавления
графического интерфейса к существующим сценариям командной строки без
реорганизации программного кода;
"""

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Demo(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        Label(self, text="Basic demos").pack()
        Button(self, text="Open", command=self.openfilename).pack(fill=BOTH)
        Button(self, text="Save", command=self.savefilename).pack(fill=BOTH)
        self.open_name = self.save_name = ""

    def openfilename(self):                     # сохранить результаты пользователя
        self.open_name = askopenfilename()      # указать параметры диалога здесь

    def savefilename(self):
        self.save_name = asksaveasfilename(initialdir="D:\Projects\Python")


if __name__ == "__main__":
    # вывести окно
    print("popup1...")
    my_dialog = Demo()              # присоединить фрейм к окну Tk() по умолчанию
    my_dialog.mainloop()            # отобразить; вернуться после закрытия окна
    print(my_dialog.open_name)      # имена сохраняются в объекте, когда окно уже
    print(my_dialog.save_name)      # будет закрыто
    # Раздел программы без графического интерфейса, использующей my_dialog

    # отобразить окно еще раз
    print("popup2...")
    my_dialog = Demo()              # повторно создать виджеты
    my_dialog.mainloop()            # повторно отобразить окно
    print(my_dialog.open_name)      # в объекте будут сохранены новые значения
    print(my_dialog.save_name)
    # Раздел программы без графического интерфейса,
    # где снова используется my_dialog
    print("ending...")


