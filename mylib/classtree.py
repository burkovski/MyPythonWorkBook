"""
classtree.py: Выполняет обход дерева наследования снизу вверх, используя ссылки на пространства
имен и отображает суперклассы с отступами.
"""


def classtree(cls, indent):
    print('.' * indent, cls.__name__)   # Вывести имя класса
    for superclass in cls.__bases__:    # Рекурсивный обход всех суперклассов
        classtree(superclass, indent+3)


def instancetree(inst):
    print("Tree of", inst)
    classtree(inst.__class__, 3)


if __name__ == "__main__":
    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(B, C):
        pass

    class E:
        pass

    class F(D, E):
        pass

    instancetree(B())
    instancetree(F())