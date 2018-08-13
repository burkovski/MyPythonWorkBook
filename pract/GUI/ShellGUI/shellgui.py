"""
инструмент запуска; использует шаблоны GuiMaker, стандартный диалог завершения
GuiMixin; это просто биб­лиотека классов: чтобы вывести графический интерфейс,
запустите сценарий mytools;
"""

from tkinter import *                                   # импортировать виджеты
from pract.GUI.Tools.guimixin import GuiMixin           # импортировать quit, а не done
from pract.GUI.Tools.guimaker import *                  # конструктор меню/панели инструментов


class ShellGUI(GuiMixin, GuiMakerWindowMenu):           # фрейм + конструктор + подмешиваемые методы
    def start(self):
        self.set_menubar()
        self.set_toolbar()
        self.master.title("Shell tools listbox")

    def handle_list(self, event):                       # двойной щелчок на списке
        label = self.listbox.get(ACTIVE)                # получить выбранный текст
        self.run_command(label)                         # и выполнить операцию

    def make_widgets(self):                             # добавить список в середину
        sbar = Scrollbar(self)                          # связать sbar со списком
        lbox = Listbox(self, bg="white")                # или использ. Tour.ScrolledList
        sbar.config(command=lbox.yview)
        lbox.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)                           # первым добавлен = посл. обрезан
        lbox.pack(side=LEFT, expand=YES, fill=BOTH)             # список обрез-ся первым
        for (label, action) in self.fetch_commands():           # добавляется в список,
            lbox.insert(END, label)                             # в меню и на панель инстр.
        lbox.bind("<Double-1>", self.handle_list)               # установить обработчик
        self.listbox = lbox

    def for_toolbar(self, label):       # поместить на панель инстр.?
        return True                     # по умолчанию = все

    def set_toolbar(self):
        self.toolbar = []
        for (label, action) in self.fetch_commands():
            if self.for_toolbar(label):
                self.toolbar.append((label, action, dict(side=LEFT)))
        self.toolbar.append(("Quit", self.quit, dict(side=RIGHT)))

    def set_menubar(self):
        tool_entries = []
        self.menubar = [
            ("File", 0, [("Quit", -1, self.quit)]),           # имя раскрывающегося меню
            ("Tools", 0, tool_entries)                      # список элементов меню: метка,клавиша,обработчик
        ]
        for (label, action) in self.fetch_commands():       # добавить приложения
            tool_entries.append((label, -1, action))        # в меню


##############################################################################
# делегирование операций шаблонным подклассам с разным способом хранения
# перечня утилит, которые в свою очередь делегируют операции
# подклассам, реализующим запуск утилит
##############################################################################


class ListMenuGUI(ShellGUI):
    def fetch_commands(self):       # myMenu устанавливается в подклассе:
        return self.my_menu         # список кортежей (метка, обработчик)

    def run_command(self, cmd):
        for (label, action) in self.my_menu:
            if label == cmd:
                action()


class DictMenuGUI(ShellGUI):
    def fetch_commands(self):
        return self.my_menu.items()

    def run_command(self, cmd):
        self.my_menu[cmd]()


