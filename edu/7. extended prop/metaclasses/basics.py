class MetaOne(type):
    def __new__(mcs, cls_name, supers, cls_dict):
        print("In MetaOne.new: ", cls_name, supers, cls_dict, sep="\n...")
        return type.__new__(mcs, cls_name, supers, cls_dict)
    def __init__(cls, cls_name, supers, cls_dict):
        print("In MetaOne.init: ", cls_name, supers, cls_dict, sep="\n...")
        print("...init class object:", list(cls.__dict__.keys()))

class Eggs:
    pass

print("Making class...")
class Spam(Eggs, metaclass=MetaOne):        # Метакласс вызывается автоматически, в конце инстукции class
    data = 1                                # Результат - класс, созданный из метакласса, а не из type
    def meth(self, n):
        pass

print("Making instance...")
X = Spam()
print("data:", X.data)
print('=' * 100)


def MetaFunc(cls_name, supers, cls_dict):
    print("In MetaFunc:", cls_name, supers, cls_dict, sep="\n...")
    return type(cls_name, supers, cls_dict)

print("Making class...")
class Spam(Eggs, metaclass=MetaFunc):       # В конце вызывает просую ф-цию
    data = 1                                # Ф-ция возвращает класс
    def meth(self, n):
        pass

print("Making instance...")
X = Spam()
print("data:", X.data)
print('=' * 100)


# Метод __call__ можно переопределить,
# а метаклассы могут иметь свои метаклассы
class SuperMeta(type):
    def __call__(meta, cls_name, supers, cls_dict):
        print("In SuperMeta.call:", cls_name, supers, cls_dict, sep="\n...")
        return type.__call__(meta, cls_name, supers, cls_dict)

class SubMeta(type, metaclass=SuperMeta):
    def __new__(mcs, cls_name, supers, cls_dict):
        print("In SubMeta.new: ", cls_name, supers, cls_dict, sep="\n...")
        return type.__new__(mcs, cls_name, supers, cls_dict)
    def __init__(cls, cls_name, supers, cls_dict):
        print("In SubMeta.init: ", cls_name, supers, cls_dict, sep="\n...")

print("Making class...")
class Spam(Eggs, metaclass=SubMeta):
    data = 1
    def meth(self, n):
        pass

print("Making instance...")
X = Spam()
print("data:", X.data)
print('=' * 100)


class SuperMeta:
    def __call__(self, cls_name, supers, cls_dict):
        print("In SuperMeta.call:", cls_name, supers, cls_dict, sep="\n...")
        cls = self.__New__(cls_name, supers, cls_dict)
        self.__Init__(cls, cls_name, supers, cls_dict)
        return cls

class SubMeta(SuperMeta):
    def __New__(self, cls_name, supers, cls_dict):
        print("In SubMeta.New:", cls_name, supers, cls_dict, sep="\n...")
        return type(cls_name, supers, cls_dict)
    def __Init__(self, cls, cls_name, supers, cls_dict):
        print("In SubMeta.Init:", cls_name, supers, cls_dict)
        print("...init class object: ", list(cls.__dict__.keys()))

print("Making class...")
class Spam(Eggs, metaclass=SubMeta()):      # Метакласс - экземпляр обычного класса, вызывается в конце инструкции
    data = 1
    def meth(self, n):
        pass

print("Making instance...")
X = Spam()
print("data:", X.data)
print('=' * 100)