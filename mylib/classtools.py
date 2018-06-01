"""
classtools.py: Различные утилиты для работы с классами
"""

class AttrDisplay:
    """
    Реализует наследуемый метод перегрузки операции вывода, отображающий
    имена классов экземплярови все атрибутыв виде пар имя=значение,
    имеющиеся в экземплярах (исключая атрибуты, кнаследованые от классов).
    Может добавляться в любые классы и способен работать с любыми экземплярами
    """
    def __gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append("{0}={1}".format(key, getattr(self, key)))
        return ', '.join(attrs)
    def __str__(self):
        return "[{0}: {1}]".format(self.__class__.__name__, self.__gatherAttrs())


class ListInstance:
    """
    Примесный класс, реализующий получение форматировангой строки при вызвове
    функций print() и str() с экземпляром в виде аргумента, через наследование
    метода __str__, реализованого здесь; отображает только атрибуты
    экземпляра; self - экземпляр самого нижнего класса в дереве наследования;
    во избежание конфликта с именами атрибутов клиентских классов использует
    имена вида __X
    """
    def __str__(self):
        return "<Instance of {0}({1}), address {2}:{3}>".format(
            self.__class__.__name__,    # Имя клиентсвкого класса
            self.__supers(),
            id(self),                   # Адрес экземпляра
            self.__attrnames()          # список пар name=value
        )
    def __attrnames(self):
        result = ""
        for attr in sorted(self.__dict__):      # Словарь атрибутов
            result += "\n\tname {0} = {1}". format(attr, self.__dict__[attr])
        return result
    def __supers(self):
        result = []
        for super in self.__class__.__bases__:
            result.append(super.__name__)
            return ', '.join(result)


class ListInherited:
    """
    Использует функцию dir() для получения списка атрибутов самого экземпляра
    и атрибутов, унаследованых экземпляром от его классов.
    Метод getattr() позволяет поулчить значения унаследованых атрибутов,
    которых нет в self.__dict__. Реализует метод __str__, а не __repr__,
    потому что в противном случае данная реализация может попасть
    в бесконечный цикл при выводе связаных методов!
    """
    def __str__(self):
        return "<Instance of {0}, address {1}:{2}>".format(
            self.__class__.__name__,    # Имя клиентсвкого класса
            id(self),                   # Адрес экземпляра
            self.__attrnames()          # список пар name=value
        )
    def __attrnames(self):
        result = ""
        for attr in dir(self):
            if attr.startswith('__') and attr.endswith('__'):
                continue
                # result += "\n\tname {}=<...>".format(attr)
            else:
                result += "\n\tname {0} = {1}". format(attr, getattr(self, attr))
        return result


class ListTree:
    """
    Примесный класс, в котором метод __str__ просматривает все дерево классов
    и составляет  список атрибутов  всех объектов, находящихся в дереве выше
    self; вызывается функциями print() и str(), возвращает сконструированую
    строку со списком; во избежание конфликтов с именами атрибутов клиентских
    классов использует имена вида __X; для ркурсивного обхода суперклассов
    использует выражение - генератор, чтобы сделать подстановку более
    очевидной, использует метод str.format()
    """
    def __str__(self):
        self.__visited = set()
        return "<Instance of {0}, address {1}:\n{2}{3}>".format(
            self.__class__.__name__,
            id(self),
            self.__attrNames(self, 0),
            self.__listClass(self.__class__, 4)
        )

    def __listClass(self, aClass, indent):
        dots = '.' * indent
        if aClass in self.__visited:
            return "\n{0}<Class {1}, address {2}: (see above)>\n".format(
                dots,
                aClass.__name__,
                id(aClass)
            )
        else:
            self.__visited.add(aClass)
            genabove = (self.__listClass(c, indent+4,) for c in aClass.__bases__)
            return "\n{0}Class {1}, address {2}:\n{3}{4}{0}>\n".format(
                dots,
                aClass.__name__,
                id(aClass),
                self.__attrNames(aClass, indent),
                ''.join(genabove)
            )

    def __attrNames(self, obj, indent):
        spaces = ' ' * (indent + 4)
        result = ''
        for attr in sorted(obj.__dict__):
            if attr.startswith('__') and attr.endswith('__'):
                result += "{0}{1}=<>\n".format(spaces, attr)
            else:
                result += "{0}{1}={2}\n".format(spaces, attr, getattr(obj, attr))
        return result



if __name__ == "__main__":
    class TopTest(AttrDisplay):
        count = 0
        def __init__(self):
            self.attr1 = TopTest.count
            self.attr2 = TopTest.count + 1
            TopTest.count += 2

    class SubTest(TopTest):
        pass

    x, y = TopTest(), SubTest()
    print(x)
    print(y)
    print()

    class Spam(ListInstance):
        def __init__(self):
            self.name = "Bob"
            self.job = "Developer"
            self.salary = 50000

    X = Spam()
    print(X)
    print()

    class Super:
        def __init__(self):
            self.data1 = "spam"

    class Sub(Super, ListTree):
        def __init__(self):
            Super.__init__(self)
            self.data2 = "eggs"
            self.data3 = 42

        def spam(self):
            pass

    X = Sub()
    print(X)
    print()