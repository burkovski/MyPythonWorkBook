"""
Расширенный Frame, автоматически создающий меню и панели инструментов в окне.
GuiMakerFrameMenu предназначен для встраивания компонентов (создает меню на
основе фреймов).
GuiMakerWindowMenu предназначен для окон верхнего уровня (создает меню Tk8.0).
Пример древовидной структуры приводится в реализации самотестирования (и
в PyEdit).
"""

from tkinter import *
from tkinter.messagebox import showinfo


class GuiMaker(Frame):
    menubar = []               # значения по умолчанию
    toolbar = []               # изменять при создании подклассов
    help_button = True         # устанавливать в start()

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)            # растягиваемый фрейм
        self.start()                                # в подклассе: установить меню/панель инстр.
        self.make_menubar()                         # здесь: создать полосу меню
        self.make_toolbar()                         # здесь: создать панель инструментов
        self.make_widgets()                         # в подклассе: добавить середину

    def make_menubar(self):
        """
        создает полосу меню вверху (реализация меню Tk8.0 приводится ниже)
        expand=no, fill=x, чтобы ширина оставалась постоянной
        """
        menubar = Frame(self, relief=RAISED, bd=2)
        menubar.pack(side=TOP, fill=X)

        for (name, key, items) in self.menubar:
            mbutton = Menubutton(menubar, text=name, underline=key)
            mbutton.pack(side=LEFT)
            pulldown = Menu(mbutton)
            self.add_menu_items(pulldown, items)
            mbutton.config(menu=pulldown)

        if self.help_button:
            Button(
                menubar,
                text="Help",
                relief=FLAT,
                command=self.help
            ).pack(side=RIGHT)

    def add_menu_items(self, menu, items):
        for item in items:                          # сканировать список вложенных элем.
            if item == "separator":                 # строка: добавить разделитель
                menu.add_separator()
            elif type(item) == list:                # список: неактивных элементов
                for num in item:
                    menu.entryconfig(num, state=DISABLED)
            elif type(item[2]) != list:
                # print(items, item, item[2])
                menu.add_command(
                    label=item[0],                  # команда: метка
                    underline=item[1],              # горячая клавиша
                    command=item[2]                 # обр-к: вызыв. объект
                )
            else:
                pullover = Menu(menu)
                self.add_menu_items(pullover, item[2])      # подменю:
                menu.add_cascade(                           # создать подменю
                    label=item[0],                          # добавить каскад
                    underline=item[1],
                    menu=pullover
                )

    def make_toolbar(self):
        """
        создает панель с кнопками внизу, если необходимо
        expand=no, fill=x, чтобы ширина оставалась постоянной
        можно добавить поддержку изображений
        """
        if self.toolbar:
            toolbar = Frame(self, cursor="hand2", relief=SUNKEN, bd=2)
            toolbar.pack(side=BOTTOM, fill=X)
            for (name, action, where) in self.toolbar:
                Button(toolbar, text=name, command=action).pack(where)

    def make_widgets(self):
        """
        'средняя' часть создается последней, поэтому меню/панель инструментов
        всегда остаются вверху/внизу и обрезаются в последнюю очередь;
        переопределите этот метод,
        для pack: прикрепляйте середину к любому краю;
        для grid: компонуйте середину по сетке во фрейме, который
        прикрепляется методом pack
        """
        name = Label(
            self,
            width=40, height=10,
            relief=SUNKEN,
            bg="white",
            text=self.__class__.__name__,
            cursor="crosshair"
        )
        name.pack(expand=YES, fill=BOTH, side=TOP)

    def help(self):
        """переопределите в подклассе"""
        showinfo("Help", "Sorry, no help for {}".format(self.__class__.__name__))

    def start(self):
        """переопределите в подклассе: связать меню/панель инструментов с self"""
        pass


GuiMakerFrameMenu = GuiMaker        # используется для меню встраиваемых компонентов


class GuiMakerWindowMenu(GuiMaker):     # используется для меню окна верхнего уровня
    def make_menubar(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        for (name, key, items) in self.menubar:
            pulldown = Menu(menubar)
            self.add_menu_items(pulldown, items)
            menubar.add_cascade(label=name, underline=key, menu=pulldown)

        if self.help_button:
            if sys.platform[:3] == "win":
                menubar.add_command(label="Help", command=self.help)
            else:           # В Linux требуется настоящее меню
                pulldown = Menu(menubar)
                pulldown.add_command(label="About", command=self.help)
                menubar.add_cascade(label="Help", menu=pulldown)


if __name__ == "__main__":
    from guimixin import GuiMixin       # встроить метод help

    menubar = [
        ("File", 0,
            [("Open", 0, lambda: 0),            # lambda:0 - пустая операция
             ("Quit", 0, sys.exit)]),            # здесь использовать sys, а не self
        ("Edit", 0,
            [("Cut", 0, lambda: 0),
             ("Paste", 0, lambda:0)])
    ]

    toolbar = [
        ("Quit", sys.exit, {'side': LEFT})
    ]


    class TestAppFrameMenu(GuiMixin, GuiMakerFrameMenu):
        def start(self):
            self.menubar = menubar
            self.toolbar = toolbar


    class TestAppWindowMenu(GuiMixin, GuiMakerWindowMenu):
        def start(self):
            self.menubar = menubar
            self.toolbar = toolbar


    class TestAppWindowMenuBasic(GuiMakerWindowMenu):
        def start(self):
            self.menubar = menubar
            self.toolbar = toolbar      # help из GuiMaker, а не из GuiMixin


    root = Tk()
    TestAppFrameMenu(Toplevel())
    TestAppWindowMenu(Toplevel())
    TestAppWindowMenuBasic(root)
    root.mainloop()
