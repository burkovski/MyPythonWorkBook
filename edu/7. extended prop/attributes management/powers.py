# 2 динамически вычесляемых атрибута, реализованных с помощью свойств
class Powers:
    def __init__(self, square, cube):
        self._square = square   # _square - базовое знчение
        self._cube = cube       # square - имя сфойства

    def getSquare(self):
        return self._square ** 2
    def setSquare(self, new_value):
        self._square = new_value
    square = property(getSquare, setSquare)

    def getCube(self):
        return self._cube ** 3
    def setCube(self, new_value):
        self._cube = new_value
    cube = property(getCube, setCube)

X = Powers(3, 4)
print(X.square, X.cube)
X.square = 5
print(X.square, X.cube)
print('-' * 10)


# Дескрипторы
class DescSquare:
    def __get__(self, instance, owner):
        return instance._square ** 2
    def __set__(self, instance, value):
        instance._square = value

class DescCube:
    def __get__(self, instance, owner):
        return instance._cube ** 3
    def __set__(self, instance, value):
        instance._cube = value

class Powers:
    square = DescSquare()
    cube = DescCube()
    def __init__(self, square, cube):
        self._square = square
        self._cube = cube

X = Powers(3, 4)
print(X.square, X.cube)
X.square = 5
print(X.square, X.cube)
print('-' * 10)


# getattr, setattr
class Powers:
    def __init__(self, square, cube):
        self._square = square
        self._cube = cube

    def __getattr__(self, item):
        if item == 'square':
            return self._square ** 2
        elif item == 'cube':
            return self._cube ** 3
        else:
            raise AttributeError(item)

    def __setattr__(self, key, value):
        if key == 'square':
            key = '_square'
        elif key == 'cube':
            key = '_cube'
        self.__dict__[key] = value

X = Powers(3, 4)
print(X.square, X.cube)
X.square = 5
print(X.square, X.cube)
print('-' * 10)
