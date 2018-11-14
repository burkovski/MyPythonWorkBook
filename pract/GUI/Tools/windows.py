"""
##############################################################################
Классы, инкапсулирующие интерфейсы верхнего уровня.
Позволяют создавать главные, всплывающие или присоединяемые окна; эти классы
могут наследоваться непосредственно, смешиваться с другими классами или
вызываться непосредственно, без создания подклассов; должны подмешиваться после
(то есть правее) более конкретных прикладных классов: иначе подклассы будут
получать методы (destroy, okayToQuit) из этих, а не из прикладных классов,
и лишатся возможности переопределить их.
##############################################################################
"""

import os
import glob
from tkinter import *
from tkinter.messagebox import showinfo, askyesno


class _window:
    """
    подмешиваемый класс, используется классами главных и всплывающих окон
    """
    found_icon = None           # совместно используется всеми экземплярами
    icon_patt = "*.ico"         # может быть сброшен
    icon_mine = "py.ico"

    def config_borders(self, app, kind, icon_file):
        if not icon_file:                       # ярлык не был передан?
            icon_file = self.find_icon()        # поиск в тек. каталоге и в каталоге модуля
        title = app
        if kind:
            title = "{}-{}".format(title, kind)
        self.title(title)                   # на рамке окна
        self.iconname(app)                 # при свертывании
        if icon_file:
            try:
                self.iconbitmap(icon_file)      # изображение ярлыка окна
            except Exception:                   # проблема с интерпретатором или платформой
                pass
        self.protocol("WM_DELETE_WINDOW", self.quit)       # не закрывать без подтверждения

    def find_icon(self):
        if _window.found_icon:               # ярлык уже найден?
            return _window.found_icon
        icon_file = None                            # сначала искать в тек. каталоге
        icons_here = glob.glob(self.icon_patt)      # допускается только один
        if icons_here:                              # удалить ярлык с красными буквами TK
            icon_file = icons_here[0]
        else:                                   # поиск в каталоге модуля
            mymod = __import__(__name__)        # импортировать, получить каталог
            path = __name__.split('.')          # возможно, путь пакета
            for mod in path[1:]:                # по всему пути до конца
                mymod = getattr(mymod, mod)     # только самый первый
            mydir = os.path.dirname(mymod.__file__)
            myicon = os.path.join(mydir, self.icon_mine)        # исп. myicon, а не tk
            if os.path.exists(myicon):
                icon_file = myicon
        _window.found_icon = icon_file           # не выполнять поиск вторично
        return icon_file


class MainWindow(Tk, _window):
    """
    главное окно верхнего уровня
    """
    def __init__(self, app, kind='', icon_file=None):
        Tk.__init__(self)
        self.__app = app
        self.config_borders(app, kind, icon_file)

    def quit(self):
        if self.okay_to_quit():       # потоки запущены?
            if askyesno(self.__app, "Verify quit program?"):
                self.destroy()        # завершить приложение
        else:
            showinfo(self.__app, "Quit not allowed!")

    def destroy(self):              # просто завершить
        Tk.quit(self)               # переопределить, если необходимо

    def okay_to_quit(self):         # переопределить, если используются
        return True                 # потоки выполнения

class PopupWindow(Toplevel, _window):
    """
    вторичное всплывающее окно
    """
    def __init__(self, app, kind='', icon_file=None):
        Toplevel.__init__(self)
        self.__app = app
        self.config_borders(app, kind, icon_file)

    def quit(self):
        if askyesno(self.__app, "Verify quit window?"):
            self.destroy()

    def destroy(self):
        Toplevel.destroy(self)


class QuietPopupWindow(PopupWindow):
    def quit(self):
        self.destroy()          # закрывать без предупреждения


class ComponentWindow(Frame):
    """
    при присоединении к другим интерфейсам
    """
    def __init__(self, parent):             # если не фрейм
        Frame.__init__(self, parent)        # предоставить контейнер
        self.pack(expand=YES, fill=BOTH)
        self.config(relief=RIDGE, border=2)     # перенастроить при необходимости

    def quit(self):
        showinfo("Quit", "Not supported in attach mode!")


